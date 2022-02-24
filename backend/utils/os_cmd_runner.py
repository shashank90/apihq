from typing import List
import subprocess
from backend.log.factory import Logger

logger = Logger(__name__)


def run_cmd(cmd_arr: List, timeout: int) -> str:
    result = None
    audit_output = None
    try:
        result = subprocess.run(
            cmd_arr,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        audit_output = result.stdout
        # Calling result.check_returncode(), raises a subprocess.CalledProcessError
        # because it detects whether completed process exited with a bad code.
        result.check_returncode()
    except subprocess.CalledProcessError as e:
        logger.error(e)
        if result:
            log_stderr(result.stderr)
    except subprocess.TimeoutExpired as e:
        logger.error(e)
        if result:
            log_stderr(result.stderr)

    return audit_output


def log_stderr(std_err):
    """
    Only log stderr if it's non-empty
    """
    if std_err:
        logger.error(std_err)
