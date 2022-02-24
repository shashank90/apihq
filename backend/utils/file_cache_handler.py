from backend.utils.constants import VALIDATER_RULE_INFO_FILE_PATH
from backend.utils.file_handler import read_json
from typing import Dict
from backend.log.factory import Logger

# Global var.
# Move to proper cache like Redis
VALIDATER_RULE_INFO = {}

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


def get_validater_rule_info():
    return VALIDATER_RULE_INFO
