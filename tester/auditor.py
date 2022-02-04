from log.factory import Logger
import subprocess
import sys
import os
from utils.constants import AUDIT_REPORT

from utils.file_handler import write_json
from utils.os_cmd_runner import run_cmd


logger = Logger(__name__)


def audit(data_dir: str, spec_path: str) -> None:
    """
    Perform OpenAPI spec audit using ibm openapi validator npm package
    """
    logger.info(f"Auditing openapi spec at {spec_path}...")

    cmd_list = ["lint-openapi", "-j", spec_path]
    audit_output = run_cmd(cmd_list, timeout=10)

    # Write audit output to spec dir
    audit_report_path = os.path.join(data_dir, AUDIT_REPORT)
    write_json(audit_report_path, audit_output)


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
