import os
from typing import Dict, List
import threading
from flask import Blueprint, jsonify, request
from apis.auth.decorators.decorator import token_required
from db.helper import (
    add_run_details,
    get_spec,
    get_run_details,
    get_api_details,
    get_run_records,
)
from db.model.api_run import ApiRun, RunStatusEnum
from db.model.api_spec import ApiSpec
from db.model.api_inventory import ApiInventory
from log.factory import Logger
from tester.modules.openapi.conformance import ISSUES_FILE, REQUESTS_FILE, run
from utils import uuid_handler
from utils.file_handler import read_json

run_bp = Blueprint("scan_bp", __name__)

logger = Logger(__name__)


@run_bp.route("/apis/v1/run/<api_id>", methods=["POST"])
@token_required
# Sample request
# { api_path: <api_path>, auth_headers: [{"<header_name1>": "<header_value1>"}, {"<header_name2>":"<header_value2>"}] }
def run_api(current_user, api_id):
    """
    Run a tests to detect if defined spec and implementation are aligned
    """
    user_id = current_user.user_id
    logger.info(f"Running API from spec {api_id} for user {user_id}")
    content = request.get_json()
    api_path = content.get("api_path")
    auth_headers = content.get("auth_headers")
    t_auth_headers = transform_headers(auth_headers)
    logger.info(f"api_path: {api_path} and auth_headers: {t_auth_headers}")

    run_id = uuid_handler.get_uuid()
    add_run_details(run_id, api_id, user_id, RunStatusEnum.INITIATED)

    api: ApiInventory = get_api_details(api_id)
    spec_id = api.spec_id
    api_path = api.api_path
    spec: ApiSpec = get_spec(spec_id)
    data_dir = spec.data_dir
    file_name = spec.file_name

    spec_path = os.path.join(data_dir, file_name)
    t = threading.Thread(
        target=run, args=[run_id, api_path, spec_path, data_dir, t_auth_headers]
    )
    t.start()

    response = jsonify({"message": "API triggered successfully"})
    response.status_code = 200

    return response


@run_bp.route("/apis/v1/runs", methods=["GET"])
@token_required
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
                    "http_method": "",
                    "status": api_run.status.name,
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

    issues_file = os.path.join(data_dir, ISSUES_FILE)
    issues: List[Dict] = read_json(issues_file)

    requests_file = os.path.join(data_dir, REQUESTS_FILE)
    requests: List[Dict] = read_json(requests_file)

    response = jsonify({"message": "success", "issues": issues, "requests": requests})

    response.status_code = 200
    return response
