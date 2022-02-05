import threading
import yaml
import json
from db.model.api_inventory import AddedByEnum
from db.model.api_spec import ApiSpec
import os
from flask import Blueprint, jsonify, request
from apis.auth.decorators.decorator import token_required
from db.helper import get_spec
from db.model.api_spec import ApiSpec
from log.factory import Logger
from tester.validator import validate
from db.model.api_spec import ApiSpec
from tester.modules.openapi.openapi_parser import get_paths
from utils.artifact_handler import (
    create_spec_artifacts,
)
from db.helper import (
    add_api_to_inventory,
    add_spec,
    get_spec,
    update_spec,
)
from utils import uuid_handler
from utils.constants import (
    CRAWLER,
    SPEC_STRING,
    VALIDATE_REPORT,
)
from utils.file_handler import read_content, write_content

X_API_SOURCE = "x-api-source"

validate_bp = Blueprint("validate_bp", __name__)

logger = Logger(__name__)


@validate_bp.route("/apis/v1/spec_strings", methods=["POST"])
@token_required
# Accept: application/json
def create_openapi_str(current_user):
    user_id = current_user.user_id
    api_id = uuid_handler.get_uuid()
    logger.info(f"Creating OpenAPI spec string for user {user_id}")

    data = request.get_json()
    collection_name: str = data["collection_name"]
    spec_string = data["spec_string"]
    # logger.info("Spec Type: " + str(type(spec_json)))

    # Identify openapi source(user or crawler)
    added_by = AddedByEnum.USER
    x_api_source = request.headers.get(X_API_SOURCE)
    if x_api_source and x_api_source == CRAWLER:
        added_by = AddedByEnum.CRAWLER

    # Create SpecParams
    spec_params = create_spec_artifacts()
    spec_id = spec_params.get_spec_id()

    data_dir = spec_params.get_data_dir()
    # Lending a name to the openapi string
    file_name = SPEC_STRING
    spec_path = os.path.join(data_dir, file_name)

    # Extract content and write to file
    content = json.loads(json.dumps(spec_string))

    write_content(spec_path, content)

    # Add spec record to specs table
    add_spec(spec_id, user_id, collection_name, file_name, data_dir)

    # Extract API paths and store in inventory table.
    # API inventory table has an FK dependency to API spec table
    path_list = get_paths(spec_path)
    for api_path, method in path_list:
        api_insert_record = {
            "user_id": user_id,
            "api_id": api_id,
            "spec_id": spec_id,
            "http_method": method,
            "added_by": added_by,
        }
        add_api_to_inventory(api_path, api_insert_record)

    # Run audit on newly created spec
    validate_output = validate(data_dir, spec_path)

    resp = jsonify(
        {
            "spec_id": spec_id,
            "message": "File created successfully",
            "validate_output": validate_output,
        }
    )
    resp.status_code = 201
    return resp


@validate_bp.route("/apis/v1/spec_strings/<spec_id>", methods=["PUT"])
@token_required
# Accept: application/json
def update_openapi_str(current_user, spec_id):
    user_id = current_user.user_id
    api_id = uuid_handler.get_uuid()
    logger.info(f"Updating OpenAPI spec string {spec_id} for user {user_id}")

    data = request.get_json()
    collection_name: str = data["collection_name"]
    spec_string: str = data["spec_string"]

    spec: ApiSpec = get_spec(spec_id)
    data_dir = spec.data_dir
    file_name = spec.file_name
    spec_path = os.path.join(data_dir, file_name)

    # Remove existing spec so that it can be overwritten with new one
    if os.path.exists(spec_path):
        os.remove(spec_path)

    # Extract content and write to file
    content = json.loads(json.dumps(spec_string))

    with open(spec_path, "w+", encoding="utf-8") as f:
        f.write(content)

    # Update spec record
    update_spec(spec_id, collection_name)

    # Update API paths in inventory table
    path_list = get_paths(spec_path)
    for api_path, method in path_list:
        api_insert_record = {
            "user_id": user_id,
            "spec_id": spec_id,
            "api_id": api_id,
            "http_method": method,
        }
        add_api_to_inventory(api_path, api_insert_record)

    # Run audit on newly created spec
    validate_output = validate(data_dir, spec_path)

    # TODO: Write audit output to file system

    resp = jsonify(
        {
            "spec_id": spec_id,
            "message": "File updated successfully",
            "validate_output": validate_output,
        }
    )
    resp.status_code = 200
    return resp


@validate_bp.route("/apis/v1/specs/<spec_id>", methods=["GET"])
@token_required
def retrieve_spec(current_user, spec_id):
    user_id = current_user.user_id

    logger.info(f"Retrieving spec {spec_id} for user {user_id}")

    spec: ApiSpec = get_spec(spec_id)
    collection_name = spec.collection_name
    data_dir = spec.data_dir
    file_name = spec.file_name
    spec_path = os.path.join(data_dir, file_name)
    validate_report_path = os.path.join(data_dir, VALIDATE_REPORT)
    validate_output = read_content(validate_report_path)

    if not os.path.exists(spec_path):
        response = jsonify(
            {
                "spec_id": spec_id,
                "message": "Spec not found",
            }
        )
        response.status_code = 404
        return response

    # response = make_response()
    # Read YAML file
    with open(spec_path, "r") as stream:
        data = yaml.safe_load(stream)
        response = jsonify(
            {
                "message": "success",
                "collection_name": collection_name,
                "spec_string": data,
                "validate_output": validate_output,
            }
        )
        response.status_code = 200
        return response


@validate_bp.route("/apis/v1/specs/validate/<spec_id>", methods=["GET"])
@token_required
def audit_api(current_user, spec_id):
    user_id = current_user.user_id
    logger.info(f"Validating API spec {spec_id} for user {user_id}...")

    spec: ApiSpec = get_spec(spec_id)
    data_dir = spec.data_dir
    file_name = spec.file_name
    spec_path = os.path.join(data_dir, file_name)

    # Run OpenAPI spec audit asynchronously
    # t = threading.Thread(target=audit, args=[data_dir, spec_path])
    # t.start()
    audit_output = validate(data_dir, spec_path)

    # TODO: Need to come up with an audit score

    response = jsonify({"message": "success", "validate_output": audit_output})
    response.status_code = 200

    return response
