from tester.connectors.zap.script_handler import add_script
from zapv2 import ZAPv2
from tester.connectors.zap.factory import get_zap
from utils.constants import DUMP_REQUEST_SCRIPT_PATH


def enable_script():
    """
    Load and enable given script
    """
    script_name = "dump_request.py"
    script_type = "httpsender"
    script_engine = "python"
    file_path = DUMP_REQUEST_SCRIPT_PATH

    zap: ZAPv2 = get_zap()
    add_script(zap, script_name, script_type, script_engine, file_path)


if __name__ == "__main__":
    enable_script()
