from tester.connectors.zap.script_handler import add_script
from zapv2 import ZAPv2
from tester.connectors.zap.factory import get_zap


def init():
    script_name = "dump_request.py"
    script_type = "httpsender"
    script_engine = "python"
    file_path = "/home/shashank/apihq/tester/connectors/zap/scripts/dump_request.py"

    zap: ZAPv2 = get_zap()
    add_script(zap, script_name, script_type, script_engine, file_path)


if __name__ == "__main__":
    init()
