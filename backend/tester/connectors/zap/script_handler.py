from zapv2 import ZAPv2

# from backend.utils.constants import ZAP_DUMP_REQUEST_SCRIPT

# from tester.connectors.zap.factory import get_zap
# from log.factory import Logger

# logger = Logger(__name__)


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


def list_scripts(zap, script_name=None):
    print("List all scripts...")
    scripts = zap.script.list_scripts
    print(scripts)


def remove_script(zap, script_name=None):
    script_name = "Test Insecure HTTP Verbs"
    print("Removing script {}", script_name)
    zap.script.remove(script_name)


def add_script(zap: ZAPv2, script_name, script_type, script_engine, file_path):
    zap.script.load(script_name, script_type, script_engine, file_path)


HOST = "http://localhost:8080"
ZAP_KEY = "tspnihgu0jdnm4ml7irhvsun5b"


class ZAP:
    def __init__(self, host, apikey=None):
        self.host = host
        # print("Initializing ZAP...")
        self.zap = ZAPv2(proxies={"http": host}, apikey=apikey)

    def get_zap(self):
        return self.zap


# Global var (Keeping a single instance)
zap_instance = ZAP(host=HOST, apikey=ZAP_KEY)


def get_zap():
    return zap_instance.get_zap()


def get_zap():
    return zap_instance.get_zap()


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
