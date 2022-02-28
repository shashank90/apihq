from zapv2 import ZAPv2

from typing import List, Dict
from backend.utils.constants import (
    ZAP_DUMP_REQUEST_SCRIPT_NAME,
    ZAP_DUMP_REQUEST_SCRIPT_PATH,
)
from backend.tester.connectors.zap.factory import get_zap
from backend.log.factory import Logger

logger = Logger(__name__)


def load(zap, script_name=None):
    script_name = "Test Insecure HTTP Verbs"
    print("Loading {} script...".format(script_name))
    zap.script.load(
        script_name,
        "active",
        "jython",
        "/home/kali/.ZAP/scripts/scripts/active/TestInsecureHTTPVerbs.py",
    )


def enable(zap, script_name=None):
    script_name = "Test Insecure HTTP Verbs"
    zap.script.enable(script_name)
    print("Enabling {} script...".format(script_name))


def list_scripts(zap: ZAPv2):
    scripts = []
    # logger.debug("List all scripts...")
    try:
        scripts = zap.script.list_scripts
        # logger.debug(scripts)
    except Exception as e:
        logger.error(f"Could not list ZAP scripts. Error: {str(e)}")
    return scripts


def is_script_enabled(zap: ZAPv2, script_name=None):
    scripts: List[Dict] = list_scripts(zap)
    for script in scripts:
        if script.get("name") == script_name:
            return True
    return False


def remove_script(zap, script_name=None):
    script_name = "Test Insecure HTTP Verbs"
    print("Removing script {}", script_name)
    zap.script.remove(script_name)


def add_script(zap: ZAPv2, script_name, script_type, script_engine, file_path):
    zap.script.load(script_name, script_type, script_engine, file_path)


def enable_request_dump_script():
    """
    Load and enable given script
    """
    script_name = ZAP_DUMP_REQUEST_SCRIPT_NAME
    script_type = "httpsender"
    script_engine = "jython"
    file_path = ZAP_DUMP_REQUEST_SCRIPT_PATH

    logger.info(f"Enabling {ZAP_DUMP_REQUEST_SCRIPT_PATH} script...")

    try:
        zap: ZAPv2 = get_zap()
        if is_script_enabled(zap, ZAP_DUMP_REQUEST_SCRIPT_NAME):
            logger.info(f"Script {ZAP_DUMP_REQUEST_SCRIPT_NAME} already enabled!")
            return

        add_script(zap, script_name, script_type, script_engine, file_path)
        if is_script_enabled(zap, ZAP_DUMP_REQUEST_SCRIPT_NAME):
            logger.info(f"Script {ZAP_DUMP_REQUEST_SCRIPT_NAME} enabled!")
    except Exception as e:
        logger.error(f"Could not enable script. Error: {str(e)}")


def init():

    script_name = "dump_request.py"
    script_type = "httpsender"
    script_engine = "jython"
    # file_path = ZAP_DUMP_REQUEST_SCRIPT
    file_path = "/home/shashank/Desktop/apihq/backend/tester/connectors/zap/scripts/dump_request.py"

    zap: ZAPv2 = get_zap()
    add_script(zap, script_name, script_type, script_engine, file_path)


if __name__ == "__main__":
    init()
