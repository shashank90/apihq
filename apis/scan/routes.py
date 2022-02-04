import os
import threading
from flask import Blueprint, jsonify, request
from apis.auth.decorators.decorator import token_required
from db.helper import get_spec
from db.model.api_spec import APISpec
from log.factory import Logger
from tester.modules.openapi.conformance import scan

scan_bp = Blueprint("scan_bp", __name__)

logger = Logger(__name__)


@scan_bp.route("/apis/v1/specs/<spec_id>/scan", methods=["POST"])
@token_required
# Sample request
# { api_path: <api_path>, auth_headers: [{"<header_name1>": "<header_value1>"}, {"header_name2":"header_value2"}] }
def scan_api(current_user, spec_id):
    """
    Run a conformance scan to detect if defined spec and implementation are aligned
    """
    user_id = current_user.user_id
    logger.info(f"Scanning API spec {spec_id} for user {user_id}")
    content = request.get_json()
    api_path = content.get("api_path")
    auth_headers = content.get("auth_headers")

    spec: APISpec = get_spec(spec_id, api_path)
    data_dir = spec.data_dir
    file_name = spec.file_name

    spec_path = os.path.join(data_dir, file_name)
    t = threading.Thread(
        target=scan, args=[api_path, spec_path, data_dir, auth_headers]
    )
    t.start()

    resp = jsonify({"message": "API Scan triggered"})
    resp.status_code = 200

    return resp
