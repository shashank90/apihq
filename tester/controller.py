import os
from typing import List

import zapv2

from core.in_memory.model.postman_collection import PostmanCollection
from misc.zap.zap_data import ZAPData
from core.service.cache_handler import get_txn_params, update_txn_params
from artifact_handler import clear_txn_data
from log.factory import Logger
from apis.discovery.target_recon.postman import parser
from apis.discovery.target_recon.postman.runner import run
from apis.discovery.target_recon.postman.util import get_target_site
from tester.connectors.zap.factory import get_zap
from tester.connectors.zap.util import get_sites
from misc.zap.scan import write_report, include_in_context, print_sites
from utils.constants import JSON_REPORT

logger = Logger(__name__)


def process_collection(path, variables=None):
    pass


# thread_pool_executor = get_thread_pool_executor()
# with ThreadPoolExecutor(max_workers=5) as executor:
# executor = ThreadPoolExecutor(5)
#     future = executor.submit(_process, (path, variables))
#     # future.add_done_callback(zap_scan_completed)
#     logger.info("Submitted Task to Thread Pool...")
#     try:
#         future.result()
#     except Exception as e:
#         print("EXCEPTION!!!", e)
# f1 = executor.submit(_process, path)
# t = threading.Thread(target=_process, args=[path])
# t.start()
# executor.shutdown(wait=False)


# TODO: Add Guard Rails at each stage to take appropriate action in case of exception
def process_collection(txn_id):
    logger.info("Processing Postman Collection...")
    txn_params = get_txn_params(txn_id)
    txn_dir: str = txn_params.get_data_dir()
    txn_id: str = txn_params.get_spec_id()

    collections: List[PostmanCollection] = txn_params.get_postman_collections()
    collection_path = collections[0].get_path()

    postman_parser = parser.Parser()
    postman_parser.parse(collection_path)

    # Extract Target site url for ZAP scan
    target_site = get_target_site(postman_parser.apis)

    # Run collection and proxy traffic through ZAP
    run(txn_params)

    # Create ZAP instance
    zap = get_zap()
    # Print sites proxied through ZAP
    sites = get_sites(zap)

    print_sites(zap)

    # Include sites into ZAP context
    ctx_name = txn_id
    ctx_id = include_in_context(zap, context_name=ctx_name, sites=sites)
    # txn_params.set_zap_data(ZAPData(ctx_name))
    update_txn_params(txn_id, zap_data=ZAPData(ctx_id, ctx_name, sites))

    # store_zap_messages(zap, txn_params, sites)

    # Print URLs proxies through ZAP
    # print_urls(zap)

    # Start active scan
    # active_scan(zap, target_site, 'Default Policy')

    # Write JSON report
    json_report = os.path.join(txn_dir, JSON_REPORT)
    write_report(json_report, zap.core.jsonreport())


def zap_scan_completed():
    logger.info("Scan completed. Please check report")


def set_form_auth(txn_id: str):
    zap = get_zap()
    # provision(zap, txn_id, form_obj)

    # TODO: Keep moving this txn lifecycle call until all txn activity is complete
    # Also move this to main method so artifacts get deleted when app is terminated ?
    close_txn(zap, txn_id)


def close_txn(zap: zapv2.ZAPv2, txn_id: str):
    clear_txn_data(zap, txn_id)
