from backend.utils.constants import (
    COMMON_PASSWORDS_FILE_PATH,
    COMMON_XSS_FILE_PATH,
    VALIDATER_RULE_INFO_FILE_PATH,
    COMMON_SQLi_FILE_PATH,
)
from backend.utils.file_handler import read_file_into_list, read_json
from typing import Dict, List
from backend.log.factory import Logger

# Global var.
# Move to proper cache like Redis
VALIDATER_RULE_INFO = {}

COMMON_PASSWORDS: List = []
COMMON_SQLi: List = []
COMMON_XSS: List = []

logger = Logger(__name__)


def cache_validater_rule_info() -> Dict:
    """
    Cache openapi validater rule info. This info contains description & examples about OAS2/OAS3/Spectral rules
    """
    logger.info("Caching validater rule info file...")
    global VALIDATER_RULE_INFO
    VALIDATER_RULE_INFO = read_json(VALIDATER_RULE_INFO_FILE_PATH)
    return VALIDATER_RULE_INFO


def init_cache():
    logger.info("Initiating file caches...")
    cache_validater_rule_info()
    cache_common_fuzz_payloads()


def get_validater_rule_info():
    return VALIDATER_RULE_INFO


def cache_common_fuzz_payloads():
    """
    Load common fuzz strings from file
    """
    logger.info("Caching common fuzz payloads...")
    global COMMON_PASSWORDS
    global COMMON_SQLi
    global COMMON_XSS
    COMMON_PASSWORDS = read_file_into_list(COMMON_PASSWORDS_FILE_PATH)
    COMMON_SQLi = read_file_into_list(COMMON_SQLi_FILE_PATH)
    # Will enable later for GET URIs only
    # COMMON_XSS = read_file_into_list(COMMON_XSS_FILE_PATH)


def get_common_passwords():
    return COMMON_PASSWORDS


def get_common_sqli():
    return COMMON_SQLi


def get_common_xss():
    return COMMON_XSS
