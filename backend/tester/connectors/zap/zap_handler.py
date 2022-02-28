from backend.utils.os_cmd_runner import run_cmd
from backend.log.factory import Logger
from backend.tester.connectors.zap.script_handler import (
    add_script,
    enable_request_dump_script,
)
from zapv2 import ZAPv2
from backend.utils.constants import (
    ZAP_DUMP_REQUEST_SCRIPT_PATH,
    ZAP_DUMP_REQUEST_SCRIPT_NAME,
)
from backend.tester.connectors.zap.factory import get_zap
from backend.utils.constants import (
    IS_ZAP_RUNNING_CHECK_LIMIT,
    ZAP_EXE,
    ZAP_KEY,
    INITIAL_ZAP_SLEEP_COUNT,
)
import os
from time import sleep
import subprocess

logger = Logger(__name__)


def start_zap():
    """
    Start zap in daemon mode
    """

    try:
        # output = run_cmd(ZAP_START_CMD, timeout=30)
        logger.info("Starting ZAP...")
        subprocess.Popen(
            [
                ZAP_EXE,
                "-daemon",
                "-addoninstall",
                "jython",
                "-config",
                "api.key=" + ZAP_KEY,
            ],
            stdout=open(os.devnull, "w"),
        )
        logger.info(f"Sleeping for {INITIAL_ZAP_SLEEP_COUNT} seconds...")
        sleep(INITIAL_ZAP_SLEEP_COUNT)
        logger.info("Done!")

        if is_zap_running(retry=True):
            enable_request_dump_script()

    except Exception:
        logger.exception("Could not start ZAP in daemon mode. Error: ")


def shutdown_zap():
    """
    Terminate zap programmatically
    """
    try:
        zap: ZAPv2 = get_zap()
        zap.core.shutdown(apikey=ZAP_KEY)
        is_zap_running()
    except Exception as e:
        logger.error(f"Could not terminate ZAP. Error: {str(e)}")


def is_zap_running(retry=False):
    """
    Use api to check if zap is running
    """
    i = 0
    logger.info("Checking if ZAP is running...")
    zap: ZAPv2 = get_zap()
    while i < IS_ZAP_RUNNING_CHECK_LIMIT:
        try:
            zap_home_path = zap.core.zap_home_path
            logger.info(f"ZAP home path {zap_home_path}")
            if zap_home_path and len(zap_home_path) > 0:
                logger.info("ZAP is running...")
                return True
        except Exception as e:
            if isinstance(e, str):
                logger.error(f"Could not connect with ZAP. Error: {e}")
            logger.error(f"Could not connect with ZAP. Error: {str(e)}")

        logger.info(
            f"Checking whether ZAP is running; Attempt: {str(i)}. Sleeping for 2 seconds"
        )
        sleep(2)
        i = i + 1

        # Retry not needed in case of ZAP termination
        if not retry:
            break

    logger.info("ZAP is not running...")
    return False


if __name__ == "__main__":
    start_zap()
