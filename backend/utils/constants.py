import os

BASE_DIR = os.getcwd()
# TODO: Replace temp with base dir

WORK_DIR = os.path.join(BASE_DIR, "logs")
DISCOVERED_DIR = "api_discovered"
data_dir = "api_spec"
DATA_DIR_PREFIX = "data_dir_"
DATA_DIR = "data_dir"
ZAP_MESSAGE_DIR = "har/zap_message_ids"
JSON_REPORT = "zap_report.json"
NEWMAN_OUTFILE = "newman_output.json"
LOG_FILE_NAME = "app"
ZAP_HTTP_PROXY = "http://localhost:8123"
TIMEOUT_SECONDS = 10
LOG_DIR = os.path.join(BASE_DIR, "logs")
UPLOAD_TXT_FILE = os.path.join(BASE_DIR, "backend/tester/modules/openapi/spam.txt")
UPLOAD_JSON_FILE = os.path.join(BASE_DIR, "backend/tester/modules/openapi/spam.json")
ALLOWED_EXTENSIONS = set(["json", "yaml", "yml"])
SAVED_REGEX_FILE = "~/Desktop/saved_regex.json"
SENSITIVE_DATA_REGEX = "sensitiveDataRegex"
OTHER_REGEX = "otherRegex"
# File with null chars. Use this to create zip bomb
DATA_FILE = "~/Desktop/bomb_data"
# TEMP HOST. DELETE AFTER TESTING
HOST = "http://localhost:8123"
VALIDATE_REPORT = "validate.json"


# Openapi sdk generation TODO: Switch based on environment
SDK_GENERATOR_CMD = "openapi-generator-cli"
PYTHON_SDK_DIR = "python_sdk"
API_DIR = os.path.join(BASE_DIR, "backend/tester/modules/openapi/python_sdk/api")
GEN_CLASSES_DIR = os.path.join(
    BASE_DIR, "backend/tester/modules/openapi/python_sdk/model"
)
OPENAPI_CONFIG_FILE = "invoker_config.json"
RUN = "run"

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
ZAP_KEY = "abcd12345"
HAR_DIR = "har"
MESSAGE = "message"
DESCRIPTION = "description"
RESPONSE_VALIDATION = "Response Validation"
ISSUE_ID = "issue_id"

SPEC_STRING = "spec_string.yaml"
YAML_LINT_ERROR_PREFIX = "Invalid YAML. Error: "

ERROR_TYPE_REQUEST = "Request Validation"
ERROR_TYPE_RESPONSE = "Response Validation"

VALIDATER_RULE_INFO_FILE_NAME = "validater_rule_info.json"
VALIDATER_RULE_INFO_FILE_PATH = os.path.join(
    BASE_DIR, "backend/utils", VALIDATER_RULE_INFO_FILE_NAME
)

# User visible messages
API_RUN_FAILED = "API Test Run failed. Please contact support"

# API Run limit
API_RUN_LIMIT = 3
DEFAULT_API_RUN_LIMIT = 3

# Http Response status
HTTP_OK = 200
HTTP_CREATED = 201
HTTP_BAD_REQUEST = 400
HTTP_UNAUTHORIZED = 401
HTTP_FORBIDDEN = 403
HTTP_RESOURCE_NOT_FOUND = 404
HTTP_INTERNAL_SERVER_ERROR = 500

# Http Response message types
ERROR = "error"
WARNING = "warning"
INFO = "info"
INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
# Error message that doesn't reveal much
GENERIC_ERROR_MESSAGE = "Something went wrong. Please contact support"

DEFAULT_LINT_ERROR_MESSAGE = "Malformed OpenAPI YAML"

# ZAP
DUMP_REQUEST_SCRIPT_RELATIVE_PATH = (
    "backend/tester/connectors/zap/scripts/dump_request.py"
)
ZAP_HOME_PATH = "zapHomePath"
ZAP_EXE = "/opt/zaproxy/zap.sh"
IS_ZAP_RUNNING_CHECK_LIMIT = 5
INITIAL_ZAP_SLEEP_COUNT = 30
ZAP_DUMP_REQUEST_SCRIPT_NAME = "Dump Request"
ZAP_DUMP_REQUEST_SCRIPT_PATH = os.path.join(
    BASE_DIR, "backend/tester/connectors/zap/scripts/dump_request.py"
)


# Form field lengths
INPUT_VALIDATION = "INPUT_VALIDATION"
COLLECTION_NAME = "Collection name"
NAME = "Name"
COLLECTION_NAME_MAX_LENGTH = 30
NAME_MAX_LENGTH = 30
PASSWORD_MAX_LENGTH = 30
COMPANY_NAME_MAX_LENGTH = 30
EMAIL_MAX_LENGTH = 40
