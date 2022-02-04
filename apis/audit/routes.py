import threading
import os
from flask import Blueprint, jsonify, request
from apis.auth.decorators.decorator import token_required
from db.helper import get_spec
from db.model.api_spec import APISpec
from log.factory import Logger
from tester.auditor import audit

audit_bp = Blueprint("audit_bp", __name__)

logger = Logger(__name__)


@audit_bp.route("/apis/v1/specs/<spec_id>/audit", methods=["GET"])
@token_required
def audit_api(current_user, spec_id):
    user_id = current_user.user_id
    logger.info(f"Auditing API spec {spec_id} for user {user_id}...")

    spec: APISpec = get_spec(spec_id)
    data_dir = spec.data_dir
    file_name = spec.file_name
    spec_path = os.path.join(data_dir, file_name)

    # Run OpenAPI spec audit asynchronously
    t = threading.Thread(target=audit, args=[data_dir, spec_path])
    t.start()

    # TODO: Need to come up with an audit score

    resp = jsonify({"message": "API Audit triggered"})
    resp.status_code = 200

    return resp
