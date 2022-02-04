from core.service.cache import get_obj, put_obj, clear_cache
from core.in_memory.model.spec_params import SpecParams
from log.factory import Logger

logger = Logger(__name__)


def put_txn_params(key: str, value):
    put_obj(key, value)


def update_txn_params(txn_id, **kwargs):
    """
    Get, update and store txn params back into cache
    :param txn_id:
    :param kwargs:
    """
    txn_params = get_txn_params(txn_id)
    for key, value in kwargs.items():
        attribute = getattr(txn_params, key)
        if isinstance(attribute, list):
            attribute.append(value)
        else:
            setattr(txn_params, key, value)
    put_txn_params(txn_id, txn_params)


def get_txn_params(key: str):
    return get_obj(key, SpecParams)


def clear_txn_params(key: str):
    try:
        logger.info(f"Removing txn_id {key} from cache")
        clear_cache(key)
    except Exception:
        logger.exception(f"Error occurred while remove txn_id {key}")
