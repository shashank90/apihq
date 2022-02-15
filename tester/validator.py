from concurrent.futures import process
from db.helper import update_validation_status
from log.factory import Logger
import re
import os
import json
from typing import List, Dict
from utils.constants import VALIDATE_REPORT
from db.model.api_validate import ValidateStatusEnum

from utils.file_handler import write_json
from utils.os_cmd_runner import run_cmd


logger = Logger(__name__)
LINT_CMD = "lint-openapi"
YAML_EXCEPTION = "YAMLException:"


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
    logger.debug(validate_out)

    try:
        validate_result: Dict = json.loads(validate_out)
        final_messages = process_validate(validate_result)
        # Write validate output to data dir
        validate_report_path = os.path.join(data_dir, VALIDATE_REPORT)
        write_json(validate_report_path, final_messages)
    except Exception as e:
        logger.exception("Could not parse validate output into json. ")
        status_enum = ValidateStatusEnum.LINT_ERROR
        status = update_validate_status(spec_id, user_id, final_messages, status_enum)

        # Could be a lint error. Return validate out as is (non-json output)
        result["validate_out"] = lint_yaml(validate_out)
        result["status"] = ValidateStatusEnum.LINT_ERROR.name
        result["is_lint_error"] = True
        return result

    # Update db status
    status = update_validate_status(spec_id, user_id, final_messages, status_enum)

    result["validate_out"] = validate_out
    result["is_lint_error"] = False
    return result


def update_validate_status(
    spec_id: str, user_id, messages: List[Dict], in_status: ValidateStatusEnum
) -> str:
    """
    Logic that makes an api ready for scan
    """
    status: str = None
    # Update validation status. Right now logic may be restrict. TODO: Come up with a score instead ?
    if len(messages) > 0:
        update_validation_status(spec_id, user_id, in_status)
    else:
        status = ValidateStatusEnum.READY_FOR_SCAN.name
        update_validation_status(spec_id, user_id, ValidateStatusEnum.READY_FOR_SCAN)
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
                path = ".".join(item["path"])
                item["path"] = path
                item[
                    "example"
                ] = "This is a good example \n for you to follow. \n Add a sample yaml"
                final_messages.append(item)

    return {"messages": final_messages}


def preprocess_validate(audit_output: str) -> str:
    """
    Preprocess audit output such that it can be displayed with proper formatting
    """
    # return re.sub( r"(^\n[Warning\]\s+[a-zA-Z\s.,\n]*).validaterc file.\n\n", "", audit_output)
    return re.sub(r"(^[Warning\]\s+[a-zA-Z\s.,\n]*).validaterc file.", "", audit_output)


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
