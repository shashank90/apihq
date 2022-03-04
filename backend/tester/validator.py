from concurrent.futures import process
from backend.db.helper import update_validation_status
from backend.log.factory import Logger
import re
import os
import json
from typing import List, Dict
from backend.utils.constants import DEFAULT_LINT_ERROR_MESSAGE, VALIDATE_REPORT
from backend.db.model.api_validate import ValidateStatusEnum
from backend.utils.file_cache_handler import get_validater_rule_info

from backend.utils.file_handler import write_json
from backend.utils.os_cmd_runner import run_cmd


logger = Logger(__name__)
LINT_CMD = "lint-openapi"
YAML_EXCEPTION = "YAMLException:"
DEFAULT_RULE_DESCRIPTION = {
    "heading": "Yet to add",
    "description": "Yet to add",
    "example": "Contact support",
}


def validate(
    data_dir: str, user_id: str, spec_id: str, spec_path: str, lint_only=False
) -> None:
    """
    Perform OpenAPI spec validation using ibm openapi validator npm package
    """
    logger.info(f"Validating openapi spec at {spec_path}...")

    validate_out: str = None
    final_messages: List = []
    status_enum = ValidateStatusEnum.FIX_VALIDATION_ERROR
    status: str = ValidateStatusEnum.FIX_VALIDATION_ERROR.name
    is_lint_error: bool = False
    result = {
        "validate_out": validate_out,
        "status": status,
        "is_lint_error": is_lint_error,
    }

    cmd_list = [LINT_CMD, "-j", spec_path]
    validate_output = run_cmd(cmd_list, timeout=10)

    validate_out = lint_yaml(validate_output)

    # Base YAML linter.Used by Import YAML Api, where we aren't even accepting file. Hence, no db update
    if lint_only:
        if validate_out:
            result["is_lint_error"] = True
        result["validate_out"] = validate_out
        return result

    validate_out: str = preprocess_validate(validate_output)

    # logger.debug(validate_out)

    validate_report_path = os.path.join(data_dir, VALIDATE_REPORT)
    try:
        validate_result: Dict = json.loads(validate_out)
        final_messages = process_validate(validate_result)
        # Write validate output to data dir
        write_json(validate_report_path, final_messages)
        validate_out = final_messages
    except Exception as e:
        logger.error(
            f"Could not deserialize validate output into json(dict) for spec_id: [{spec_id}]. Error: {str(e)}"
        )
        status_enum = ValidateStatusEnum.LINT_ERROR
        status = update_validate_status(spec_id, user_id, None, status_enum)

        # Could be a lint error. Return validate out as is (non-json output)
        if validate_out and len(validate_out) > 0:
            lint_out = lint_yaml(validate_out)
            lint_error_message = get_default_lint_error_message(lint_out)
            result["validate_out"] = get_lint_error_msg(lint_error_message)
            logger.info(
                f"Hence writing validate_output directly to file for spec_id: [{spec_id}]"
            )
            write_json(validate_report_path, lint_error_message)
        else:
            lint_error_message = get_default_lint_error_message(None)
            result["validate_out"] = get_lint_error_msg(lint_error_message)
            write_json(validate_report_path, lint_error_message)

        result["status"] = ValidateStatusEnum.LINT_ERROR.name
        result["is_lint_error"] = True
        return result

    # Update db status
    status = update_validate_status(spec_id, user_id, final_messages, status_enum)

    result["validate_out"] = validate_out
    result["status"] = status
    result["is_lint_error"] = False
    return result


def get_lint_error_msg(lint_error_msg: Dict) -> str:
    """
    Extract lint error message from message list
    """
    lint_error_msgs = lint_error_msg.get("messages")
    if len(lint_error_msgs) > 0:
        return lint_error_msgs[0].get("message")
    return DEFAULT_LINT_ERROR_MESSAGE


def get_default_lint_error_message(validate_out):
    """
    Default lint error message to be written to json file
    """
    if validate_out:
        return {"messages": [{"message": validate_out, "path": "", "line": ""}]}
    return {
        "messages": [
            {
                "message": DEFAULT_LINT_ERROR_MESSAGE,
                "path": "",
                "line": "",
                "rule": "malformed-spec",
            }
        ]
    }


def update_validate_status(
    spec_id: str, user_id, message_object: Dict, in_status: ValidateStatusEnum
) -> str:
    """
    Logic that makes an api ready for scan
    """
    status: str = None
    if message_object:
        messages = message_object.get("messages")
        # Update validation status. Right now logic may be restrict. TODO: Come up with a score instead ?
        if len(messages) > 0:
            update_validation_status(spec_id, user_id, in_status)
        else:
            update_validation_status(spec_id, user_id, ValidateStatusEnum.RUN_API)
            status = ValidateStatusEnum.RUN_API.name
    else:
        status = in_status.name
        update_validation_status(spec_id, user_id, in_status)

    return status


def process_validate(validate_out: Dict) -> Dict:
    """
    Join path array into '.' separated string and add example for given validation error wherever possible
    """
    # Merge errors and warnings for now.
    # TODO: Need to come up with priority/score for each error/warning message

    final_messages = []
    for key, items in validate_out.items():
        if key == "errors" or key == "warnings":
            for item in items:
                rule_description = get_rule_description(item["rule"])
                path = ".".join(item["path"])
                item["path"] = path
                item["heading"] = rule_description.get("heading")
                item["description"] = rule_description.get("description")
                item["example"] = rule_description.get("example")
                final_messages.append(item)

    return {"messages": final_messages}


def get_rule_description(rule):
    validater_info_rules: List[Dict] = get_validater_rule_info()
    for info_obj in validater_info_rules:
        info_rule = info_obj["rule"]
        if info_rule == rule:
            return info_obj["info"]
    return DEFAULT_RULE_DESCRIPTION


def preprocess_validate(audit_output: str) -> str:
    """
    Preprocess audit output such that it can be displayed with proper formatting
    """
    return re.sub(r"(^[Warning\]\s+['_\-()a-zA-Z\s.,\n]*)", "", audit_output)


def lint_yaml(audit_output: str) -> str:
    """
    Lint YAML. Return None if no linting problems
    """
    if YAML_EXCEPTION in audit_output:
        return audit_output.split(YAML_EXCEPTION)[1].rstrip("^")
    return None


def get_parent_dir(spec_path):
    """
    TODO: Remove this hack of getting parent dir from openapi spec path. Instead get txn_dir from txn_params
    """
    return os.path.dirname(os.path.abspath(spec_path))


def log_stderr(std_err):
    """
    Only log stderr if it's non-empty
    """
    if std_err:
        logger.error(std_err)
