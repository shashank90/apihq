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


def validate(data_dir: str, spec_id: str, spec_path: str, lint_only=False) -> None:
    """
    Perform OpenAPI spec audit using ibm openapi validator npm package
    """
    logger.info(f"Validating openapi spec at {spec_path}...")

    cmd_list = [LINT_CMD, "-j", spec_path]
    validate_output = run_cmd(cmd_list, timeout=10)

    # Base YAML linter
    if lint_only:
        validate_out = lint_yaml(validate_output)
        return validate_out

    validate_out: str = preprocess_validate(validate_output)
    # logger.info(validate_out)
    # logger.info("Type: " + str(type(validate_out)))

    validate_result: Dict = json.loads(validate_out)
    # logger.info(validate_result)

    final_messages = process_validate(validate_result)

    # Update db status
    update_validate_status(spec_id, final_messages)

    # Write validate output to data dir
    validate_report_path = os.path.join(data_dir, VALIDATE_REPORT)
    write_json(validate_report_path, final_messages)

    return final_messages


def update_validate_status(spec_id: str, messages: List[Dict]):
    """
    Logic that makes an api ready for scan
    """
    # Update validation status. Right now logic may be restrict. TODO: Come up with a score instead ?
    if len(messages) > 0:
        update_validation_status(spec_id, ValidateStatusEnum.FIX_VALIDATION_ERROR)
    else:
        update_validation_status(spec_id, ValidateStatusEnum.READY_FOR_SCAN)


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
