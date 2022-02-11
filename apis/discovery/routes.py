import hashlib
import yaml
import os
import shutil
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from tester.validator import validate
from apis.auth.decorators.decorator import token_required
from db.helper import (
    add_api_to_inventory,
    add_spec,
    get_api_inventory,
)
from db.model.api_inventory import ApiInventory, AddedByEnum
from tester.modules.openapi.openapi_parser import get_paths
from utils import uuid_handler

from utils.artifact_handler import (
    create_spec_artifacts,
)
from log.factory import Logger
from utils.constants import (
    CRAWLER,
    ALLOWED_EXTENSIONS,
    SPEC_STRING,
    UNNAMED,
    YAML_LINT_ERROR_PREFIX,
)

X_API_SOURCE = "x-api-source"


def allowed_openapi_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


logger = Logger(__name__)

discovery_bp = Blueprint("discovery_bp", __name__)


@discovery_bp.route("/apis/v1/specs", methods=["POST"])
@token_required
# Accept: multipart/form-data
def import_api(current_user):
    user_id = current_user.user_id
    logger.info(f"Uploading OpenAPI spec for user {user_id}")

    # Identify openapi source(user or crawler)
    added_by = AddedByEnum.USER
    x_api_source = request.headers.get(X_API_SOURCE)
    if x_api_source and x_api_source == CRAWLER:
        added_by = AddedByEnum.CRAWLER

    # Deserialize form-data to extract collection name
    collection_name = request.form.get("collection_name", UNNAMED)

    # Check if the post request has the file part
    if "file" not in request.files:
        # if "file" not in form_data:
        response = jsonify({"message": "No file part in the request"})
        response.status_code = 400
        return response
    # file = form_data["file"]
    file = request.files["file"]
    if file.filename == "":
        response = jsonify({"message": "No file selected for uploading"})
        response.status_code = 400
        return response
    if file and allowed_openapi_file(file.filename):
        file_name = secure_filename(file.filename)

        # Create SpecParams
        spec_params = create_spec_artifacts()
        spec_id = spec_params.get_spec_id()

        data_dir = spec_params.get_data_dir()
        spec_path = os.path.join(data_dir, file_name)

        # Save file on the file system(data dir)
        file.save(spec_path)

        # Lint and check if valid YAML
        response = {}
        lint_output = validate(data_dir, spec_id, spec_path, lint_only=True)
        if lint_output:
            error_msg = YAML_LINT_ERROR_PREFIX + lint_output
            response = jsonify({"error": {"message": error_msg}})
            response.status_code = 400
            # Remove data dir
            logger.info(f"Incoming YAML lint failed. Removing data dir {data_dir}")
            shutil.rmtree(data_dir)
            return response

        # Add spec record to specs table
        add_spec(spec_id, user_id, collection_name, file_name, data_dir)

        # Extract API paths and store in inventory table.
        # API inventory table has an FK dependency to API spec table
        path_list = get_paths(spec_path)
        for api_path, method, api_endpoint_url in path_list:
            api_id = uuid_handler.get_uuid()
            api_insert_record = {
                "user_id": user_id,
                "api_id": api_id,
                "api_endpoint_url": api_endpoint_url,
                "spec_id": spec_id,
                "http_method": method,
                "added_by": added_by,
            }
            add_api_to_inventory(user_id, api_path, api_insert_record)

        response = jsonify(
            {"spec_id": spec_id, "message": "File uploaded successfully"}
        )

        response.status_code = 201
        return response
    else:
        response = jsonify(
            {"error": {"message": "Only OpenAPI in YAML format is supported"}}
        )
        response.status_code = 400
        return response


def allowed_discovery_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@discovery_bp.route("/apis/v1/discover/agent", methods=["POST"])
@token_required
def discover_api(current_user):
    """
    Receive apis from code repository crawler
    """
    user_id = current_user.user_id
    api_records = request.get_json()
    # Insert APIs discovered from code repository into inventory
    for api_record in api_records:
        api_id = uuid_handler.get_uuid()
        api_path = api_record.get("api_path")
        http_method = api_record.get("http_method")
        found_in_file = api_record.get("found_in_file")
        api_insert_record = {
            "user_id": user_id,
            "api_id": api_id,
            "http_method": http_method,
            "added_by": AddedByEnum.CRAWLER,
            "user_id": user_id,
            "found_in_file": found_in_file,
        }

        add_api_to_inventory(user_id, api_path, api_insert_record)
    # Respond
    resp = jsonify(
        {
            "message": "Updated inventory with newly discovered APIs",
        }
    )
    resp.status_code = 201

    return resp


@discovery_bp.route("/apis/v1/discovered", methods=["GET"])
@token_required
def get_discovered_apis(current_user):
    """
    Return discovered APIs from inventory table
    """
    user_id = current_user.user_id
    logger.info(f"Returning APIs discovered for user {user_id}")
    api_list = get_api_inventory(user_id)

    apis = [
        {
            "spec_id": api.spec_id,
            "api_path": api.api_path,
            "api_endpoint_url": api.api_endpoint_url,
            "http_method": api.http_method,
            "added_by": api.added_by.name,
            "message": api.message,
        }
        for api in api_list
    ]

    resp = jsonify({"message": "success", "apis": apis})
    resp.status_code = 200
    return resp


def store_file(file):
    file_name = file.filename
    logger.info(f"Saving target recon file {file_name}")
    contents = file.read()
    md5_hash = hashlib.md5()
    md5_hash.update(contents)
    digest = md5_hash.hexdigest()
