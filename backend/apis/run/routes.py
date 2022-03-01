from http.client import HTTPResponse
import os
from typing import Dict, List
import threading
from marshmallow import validate, ValidationError
from backend.apis.model.http_error import HttpResponse
from flask import Blueprint, jsonify, request
from backend.apis.auth.decorators.decorator import token_required
from backend.apis.input_validator.validator import is_api_run_limit_exceeded
from backend.apis.response_handler.decorator import handle_response
from backend.db.helper import (
    add_run_details,
    get_spec,
    get_run_details,
    get_api_details,
    get_run_records,
)
from backend.db.model.api_run import ApiRun, RunStatusEnum
from backend.db.model.api_spec import ApiSpec
from backend.db.model.api_inventory import ApiInventory
from backend.log.factory import Logger
from backend.tester.modules.openapi.conformance import ISSUES_FILE, REQUESTS_FILE, run
from backend.utils import uuid_handler
from backend.utils.file_handler import get_run_dir_path, read_json
from backend.utils.constants import (
    HTTP_BAD_REQUEST,
    ERROR,
)

run_bp = Blueprint("run_bp", __name__)

logger = Logger(__name__)

API_RUN_LIMIT_EXCEEDED = "API_RUN_LIMIT_EXCEEDED"


@run_bp.route("/apis/v1/run/<api_id>", methods=["POST"])
@token_required
@handle_response
# Sample request
# { api_path: <api_path>, auth_headers: [{"<header_name1>": "<header_value1>"}, {"<header_name2>":"<header_value2>"}] }
def run_api(current_user, api_id):
    """
    Run a tests to detect if defined spec and implementation are aligned
    """
    user_id = current_user.user_id
    logger.info(f"Running API {api_id} for user {user_id}")
    content = request.get_json()
    api_endpoint_url = content.get("api_endpoint_url")
    http_method = content.get("http_method")
    auth_headers = content.get("auth_headers")

    t_auth_headers = transform_headers(auth_headers)
    logger.info(
        f"api_endpoint_url: {api_endpoint_url}; http method :{http_method} auth_headers: {t_auth_headers}"
    )
    if is_api_run_limit_exceeded(user_id):
        raise HttpResponse(
            message="API Run limit for user exceeded",
            code=API_RUN_LIMIT_EXCEEDED,
            http_status=HTTP_BAD_REQUEST,
            type=ERROR,
        )

    run_id = uuid_handler.get_uuid()
    add_run_details(run_id, api_id, user_id, RunStatusEnum.INITIATED)

    api: ApiInventory = get_api_details(api_id)
    spec_id = api.spec_id
    api_endpoint_url = api.api_path
    spec: ApiSpec = get_spec(spec_id)
    data_dir = spec.data_dir
    file_name = spec.file_name

    spec_path = os.path.join(data_dir, file_name)
    t = threading.Thread(
        target=run, args=[run_id, api_endpoint_url, spec_path, data_dir, t_auth_headers]
    )
    t.start()

    response = jsonify({"message": "API Tests triggered successfully"})
    response.status_code = 200

    return response


@run_bp.route("/apis/v1/runs", methods=["GET"])
@token_required
@handle_response
def get_runs(current_user):
    """
    Run a tests to detect if defined spec and implementation are aligned
    """
    user_id = current_user.user_id
    logger.info(f"Fetching API runs for user {user_id}")

    api_runs: List[ApiRun] = get_run_records(user_id)
    runs = []
    if api_runs:
        for api_run in api_runs:
            runs.append(
                {
                    "run_id": api_run.run_id,
                    "api_endpoint_url": api_run.api.api_endpoint_url,
                    "http_method": api_run.api.http_method,
                    "status": api_run.status.name,
                    "message": api_run.message,
                    "updated": api_run.time_updated,
                }
            )

    response = jsonify({"message": "success", "runs": runs})
    response.status_code = 200

    return response


def transform_headers(auth_headers: List[Dict]):
    """
    Transform headers from [{'headerName':'x-access-token', 'headerValue':'token123'}] to [{'x-access-token':'token123'}]
    """
    return [{item["headerName"]: item["headerValue"]} for item in auth_headers]


@run_bp.route("/apis/v1/issues/<run_id>", methods=["GET"])
@token_required
@handle_response
def get_issues(current_user, run_id):
    """
    Run a tests to detect if defined spec and implementation are aligned
    """
    user_id = current_user.user_id
    logger.info(f"Fetching issues for run {run_id} for user {user_id}")

    api_run: ApiRun = get_run_details(run_id)
    api_id = api_run.api_id
    api: ApiInventory = get_api_details(api_id)
    spec_id = api.spec_id
    spec: ApiSpec = get_spec(spec_id)
    data_dir: str = spec.data_dir

    run_dir = get_run_dir_path(data_dir, run_id)
    issues_file = os.path.join(run_dir, ISSUES_FILE)
    issues: List[Dict] = read_json(issues_file)

    requests_file = os.path.join(run_dir, REQUESTS_FILE)
    requests: List[Dict] = read_json(requests_file)

    response = jsonify({"message": "success", "issues": issues, "requests": requests})

    response.status_code = 200
    return response
