import os

BASE_DIR = "~/apihq"
# TODO: Replace temp with base dir
TEMP_DIR = "/home/shashank/Desktop/apihq"

WORK_DIR = os.path.join(TEMP_DIR, "logs")
DISCOVERED_DIR = "api_discovered"
data_dir = "api_spec"
DATA_DIR_PREFIX = "data_dir_"
DATA_DIR = "data_dir"
ZAP_MESSAGE_DIR = "har/zap_message_ids"
UPLOAD_FOLDER = "~/apihq/logs"
JSON_REPORT = "zap_report.json"
NEWMAN_OUTFILE = "newman_output.json"
LOG_FILE_NAME = "app"
ZAP_HTTP_PROXY = "http://localhost:8123"
TIMEOUT_SECONDS = 10
LOG_DIR = os.path.join(TEMP_DIR, "logs")
UPLOAD_TXT_FILE = os.path.join(TEMP_DIR, "tester/modules/openapi/spam.txt")
UPLOAD_JSON_FILE = os.path.join(TEMP_DIR, "tester/modules/openapi/spam.json")
ALLOWED_EXTENSIONS = set(["json", "yaml", "yml"])
SAVED_REGEX_FILE = "~/Desktop/saved_regex.json"
SENSITIVE_DATA_REGEX = "sensitiveDataRegex"
OTHER_REGEX = "otherRegex"
# File with null chars. Use this to create zip bomb
DATA_FILE = "~/Desktop/bomb_data"
# TEMP HOST. DELETE AFTER TESTING
HOST = "http://localhost:8123"
VALIDATE_REPORT = "validate.json"
PYTHON_SDK_DIR = "python_sdk"
API_DIR = os.path.join(TEMP_DIR, "tester/modules/openapi/python_sdk/api")
GEN_CLASSES_DIR = os.path.join(TEMP_DIR, "tester/modules/openapi/python_sdk/model")
OPENAPI_CONFIG_FILE = "invoker_config.json"
REQUEST_ID = "request_id"
CRLF = "\r\n"
PACKAGE_NAME = "packageName"
SDK_DIR = "python_sdk"
MODEL_DIR = "model"
API_DIR = "api"
TEMP_FOLDER_SUFFIX = "_1"
FILE_ATTRIBUTE_TYPE = "file"
CRAWLER = "crawler"
UNNAMED = "unnamed"

# TODO: ZAP KEY. Need to move this to config file
ZAP_KEY = "tspnihgu0jdnm4ml7irhvsun5b"
HAR_DIR = "har"
MESSAGE = "message"
DESCRIPTION = "description"
RESPONSE_VALIDATION = "Response Validation"
ISSUE_ID = "issue_id"

SPEC_STRING = "spec_string.yaml"
YAML_LINT_ERROR_PREFIX = "Invalid YAML uploaded. Error: "

ERROR_TYPE_REQUEST = "Request Validation"
ERROR_TYPE_RESPONSE = "Response Validation"

VALIDATER_RULE_INFO_FILE_NAME = "validater_rule_info.json"
VALIDATER_RULE_INFO_FILE_PATH = os.path.join(
    TEMP_DIR, "utils", VALIDATER_RULE_INFO_FILE_NAME
)
