# Txn lifecycle methods
import uuid

import zapv2
from backend.in_memory.model.discovery_params import DiscoveryParams

from backend.in_memory.model.spec_params import SpecParams
from backend.log.factory import Logger
from backend.utils.file_handler import create_spec_folder

logger = Logger(__name__)


def clear_txn_data(zap: zapv2.ZAPv2, txn_id):
    """
    This is a Txn lifecycle method. It's used to clear txn related artifacts
    :param zap: ZAP instance
    :param txn_id: txn_id
    """
    # txn_params: SpecParams = get_txn_params(txn_id)
    # zap_data: ZAPData = txn_params.get_zap_data()
    # Remove ZAP related artifacts
    # clear_zap_data(zap, zap_data)
    # Remove from cache
    # clear_txn_params(txn_id)
    pass


def create_spec_artifacts() -> SpecParams:
    """
    Create folder for storing openapi specs
    """
    spec_id = generate_spec_id()
    data_dir = create_spec_folder(spec_id)
    logger.info(f"Created folder [{data_dir}] for storing openapi specs")
    spec_params = SpecParams(spec_id, data_dir)
    return spec_params


def generate_spec_id() -> str:
    """
    Generate randome & unique spec id
    """
    spec_id = "S" + uuid.uuid4().hex
    return spec_id


def generate_discovery_id() -> str:
    """
    Generate random & unique discovery id
    """
    disc_id = "D" + uuid.uuid4().hex
    return disc_id
