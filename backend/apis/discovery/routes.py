import os
import shutil
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from backend.apis.input_validator.validator import is_invalid_name
from backend.apis.response_handler.decorator import handle_response
from backend.db.model.api_validate import ValidateStatusEnum
from backend.tester.validator import validate
from backend.apis.auth.decorators.decorator import token_required
from backend.db.helper import (
    add_api_to_inventory,
    add_spec,
    delete_api_record,
    get_api_inventory,
    get_api_status,
)
from backend.apis.model.http_error import HttpResponse
from backend.db.model.api_inventory import AddedByEnum
from backend.tester.modules.openapi.openapi_parser import get_paths
from backend.utils import uuid_handler
from backend.utils.api_helper import convert_postman_collection

from backend.utils.artifact_handler import (
    create_spec_artifacts,
)
from backend.log.factory import Logger
from backend.utils.constants import (
    ALLOWED_OPENAPI_EXTENSIONS,
    API_DELETE_FAILED,
    COLLECTION_NAME,
    COLLECTION_NAME_MAX_LENGTH,
    CRAWLER,
    ALLOWED_EXTENSIONS,
    ERROR,
    HTTP_BAD_REQUEST,
    HTTP_INTERNAL_SERVER_ERROR,
    INPUT_VALIDATION,
    OPENAPI_POSTMAN_COLLECTION,
    OPENAPI_SUPPORTED_FILE_TYPE,
    UNNAMED,
    UNSUPPORTED_OPENAPI_FILE_TYPE,
    YAML_LINT_ERROR_PREFIX,
    POSTMAN_COLLECTION,
    FILE_NAME,
    FILE_NAME_MAX_LENGTH,
    OpenAPI,
)
from backend.utils.file_handler import get_file_name_and_extension, remove_data_dir

X_API_SOURCE = "x-api-source"


def allowed_openapi_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


logger = Logger(__name__)

discovery_bp = Blueprint("discovery_bp", __name__)


@discovery_bp.route("/apis/v1/specs", methods=["POST"])
@token_required
@handle_response
# Accept: multipart/form-data
def import_api(current_user):
    user_id = current_user.user_id
    logger.info(f"Uploading OpenAPI spec for user: [{user_id}]")

    # Identify openapi source(user or crawler)
    added_by = AddedByEnum.USER
    x_api_source = request.headers.get(X_API_SOURCE)
    if x_api_source and x_api_source == CRAWLER:
        added_by = AddedByEnum.CRAWLER

    # Deserialize form-data to extract collection name
    collection_name = request.form.get("collection_name", UNNAMED)

    file_type = request.form.get("file_type", UNNAMED)

    message = is_invalid_name(
        COLLECTION_NAME, collection_name, COLLECTION_NAME_MAX_LENGTH
    )
    if message:
        raise HttpResponse(
            message=message,
            code=INPUT_VALIDATION,
            http_status=HTTP_BAD_REQUEST,
            type=ERROR,
        )

    # Check if the post request has the file part
    if "file" not in request.files:
        response = jsonify({"message": "No file part in the request"})
        response.status_code = 400
        return response
    file = request.files["file"]
    if file.filename == "":
        response = jsonify({"message": "No file selected for uploading"})
        response.status_code = 400
        return response
    if file and allowed_openapi_file(file.filename):
        file_name = secure_filename(file.filename)
        f_name, _ = get_file_name_and_extension(file_name)

        # Check file name length
        message = is_invalid_name(FILE_NAME, f_name, FILE_NAME_MAX_LENGTH)
        if message:
            raise HttpResponse(
                message=message,
                code=INPUT_VALIDATION,
                http_status=HTTP_BAD_REQUEST,
                type=ERROR,
            )

        # Create SpecParams
        spec_params = create_spec_artifacts()
        spec_id = spec_params.get_spec_id()

        data_dir = spec_params.get_data_dir()
        spec_path = os.path.join(data_dir, file_name)

        # Save file on the file system(data dir)
        file.save(spec_path)

        if file_type == POSTMAN_COLLECTION:
            (
                converted_spec_path,
                updated_file_name,
                conversion_out_message,
            ) = convert_postman_collection(user_id, data_dir, file_name, spec_path)
            if conversion_out_message:
                raise HttpResponse(
                    message=conversion_out_message,
                    code=INPUT_VALIDATION,
                    http_status=HTTP_BAD_REQUEST,
                    type=ERROR,
                )
            # Set new spec path after conversion(postman collection -> openapi)
            spec_path = converted_spec_path
            file_name = updated_file_name

        elif file_type == OpenAPI:
            _, file_extension = get_file_name_and_extension(file.filename)
            if file_extension.strip(".") not in ALLOWED_OPENAPI_EXTENSIONS:
                raise HttpResponse(
                    message=OPENAPI_SUPPORTED_FILE_TYPE,
                    code=UNSUPPORTED_OPENAPI_FILE_TYPE,
                    http_status=HTTP_BAD_REQUEST,
                    type=ERROR,
                )

        # Lint and check if valid YAML
        response = {}
        output = validate(data_dir, user_id, spec_id, spec_path, lint_only=True)
        is_lint_error = output.get("is_lint_error")
        lint_output = output.get("validate_out")
        if is_lint_error:
            # Rejecting file and hence removing data dir
            remove_data_dir(data_dir)

            error_msg = YAML_LINT_ERROR_PREFIX + lint_output
            raise HttpResponse(
                message=error_msg,
                code=INPUT_VALIDATION,
                http_status=HTTP_BAD_REQUEST,
                type=ERROR,
            )

        # Add spec record to specs table
        add_spec(spec_id, user_id, collection_name, file_name, data_dir)

        # Extract API paths and store in inventory table.
        # API inventory table has an FK dependency to API spec table
        try:
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
        except Exception as e:
            logger.error(
                f"Could not extract paths from OpenAPI spec. Uploaded file {spec_path} may not adhere to OpenAPI standard. Error: {str(e)}"
            )

        # Add validation status entry for uploaded file
        validate(data_dir, user_id, spec_id, spec_path)

        response = jsonify(
            {"spec_id": spec_id, "message": "File uploaded successfully"}
        )
        response.status_code = 201
        return response
    else:
        raise HttpResponse(
            message=OPENAPI_POSTMAN_COLLECTION,
            code=UNSUPPORTED_OPENAPI_FILE_TYPE,
            http_status=HTTP_BAD_REQUEST,
            type=ERROR,
        )


def allowed_discovery_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@discovery_bp.route("/apis/v1/discovered", methods=["GET"])
@token_required
@handle_response
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
            "status": get_api_status(api.spec_id),
            "api_id": api.api_id,
            "api_path": api.api_path,
            "api_endpoint_url": api.api_endpoint_url,
            # coma separated http methods (string)
            "http_method": api.http_method,
            "added_by": api.added_by.name,
            "message": api.message,
            "collection_name": api.spec.collection_name if api.spec else "",
            "updated": api.time_updated,
        }
        for api in api_list
    ]

    # Query param to fetch apis with given status
    status = request.args.get("status")
    if status:
        apis = list(filter(lambda d: d["status"] == status, apis))

    response = jsonify({"message": "success", "apis": apis})
    response.status_code = 200
    return response


@discovery_bp.route("/apis/v1/discover/agent", methods=["POST"])
@token_required
@handle_response
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


@discovery_bp.route("/apis/v1/apis/<api_id>", methods=["DELETE"])
@token_required
@handle_response
def delete_api(current_user, api_id):
    """
    Delete api given api_id
    """
    user_id = current_user.user_id
    logger.info(f"Deleting api: [{api_id}] by user: [{user_id}]")

    # Deleting api only and not corresponding spec
    success = delete_api_record(api_id)

    if success:
        resp = jsonify(
            {
                "api_id": api_id,
                "message": "Deleted API successfully",
            }
        )
        resp.status_code = 200
        return resp
    else:
        raise HttpResponse(
            message="API Delete failed. Check logs for details",
            code=API_DELETE_FAILED,
            http_status=HTTP_INTERNAL_SERVER_ERROR,
            type=ERROR,
        )
