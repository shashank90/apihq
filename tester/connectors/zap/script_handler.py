import zapv2

from log.factory import Logger

logger = Logger(__name__)


def load(zap, script_name=None):
    script_name = "Test Insecure HTTP Verbs"
    print("Loading {} script...".format(script_name))
    zap.script.load(script_name, "active", "jython", "/home/kali/.ZAP/scripts/scripts/active/TestInsecureHTTPVerbs.py")


def enable(zap, script_name=None):
    script_name = "Test Insecure HTTP Verbs"
    zap.script.enable(script_name)
    print("Enabling {} script...".format(script_name))


def list_scripts(zap, script_name=None):
    print("List all scripts...")
    scripts = zap.script.list_scripts
    print(scripts)


def remove_script(zap, script_name=None):
    script_name = 'Test Insecure HTTP Verbs'
    print("Removing script {}", script_name)
    zap.script.remove(script_name)


def add_script(zap: zapv2.ZAPv2):
    script_name = 'simple_auth.js'
    logger.info(f"Loading and enabling auth script {script_name}")
    script_type = 'authentication'
    script_engine = 'Oracle Nashorn'
    file_name = '/home/kali/Desktop/appsechq-custom-scripts/zap/authentication/simple_auth.js'
    zap.script.load(script_name, script_type, script_engine, file_name)
