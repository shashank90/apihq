from typing import Dict, List
import json
from zapv2 import ZAPv2

from backend.utils.constants import REQUEST_ID

from backend.log.factory import Logger

logger = Logger(__name__)

HOST = "http://localhost:8080"


def get_urls(zap: ZAPv2, site=None):
    urls = []
    try:
        urls = zap.core.urls(baseurl=site)
    # for url in urls:
    #     logger.info(url)
    except Exception as e:
        logger.exception("Error occurred while getting urls ")
        # pass
    return urls


def get_sites(zap: ZAPv2) -> List[str]:
    sites = []
    try:
        sites = zap.core.sites
    except Exception as e:
        logger.exception("Error occurred while fetching sites")
        # pass
    return sites


def _get_messages(zap: ZAPv2, sites: List[str]) -> List:
    zap.core.messages()
    """
    Get all request/response message(dict) sent by ZAP
    :param zap: ZAP instance
    :param sites: Site node
    :return: List of messages
    """
    messages = []
    for site in sites:
        messages.extend(get_message(zap, baseURL=site))
    return messages


# TODO: Might need some fine-tuning(in terms of storage) in case there are many requests
def get_message(zap: ZAPv2, baseURL=None) -> List:
    """
    Gets the HTTP messages sent by ZAP, request and response, optionally filtered by URL
    :param zap: ZAP instance
    """
    messages = []
    try:
        messages.extend(zap.core.messages(baseURL))
    except Exception:
        logger.exception("Error occurred while fetching messages")
        # pass
    return messages


def get_messages(zap):
    sites = get_sites(zap)
    return _get_messages(zap, sites)


def get_messages_from_zap(messages):
    """
    Get messages proxied through zap in this format: {"url": "", "zap_message_id": "", request_id: ""}
    """
    url_details = []
    for message in messages:
        id = message["id"]

        req_headers = message["requestHeader"]
        temp = req_headers.split(" ")

        url = temp[1]
        request_id = get_request_id_header(temp)
        url_detail = {"zap_message_id": id, "url": url, "request_id": request_id}
        url_details.append(url_detail)

    return url_details


def get_zap_message_detail(request_id: str, url: str, zap_messages: List[Dict]):
    """
    Given a request id, fetch zap message. Example structure: [{'request_id':'R1', 'zap_message_id':'M1', 'request_id':'R2', 'zap_message_id':'M2'}]
    """
    filtered: List = filter(
        lambda x: x["request_id"] == request_id and x["url"] == url, zap_messages
    )
    if filtered:
        filter_list = list(filtered)
        if len(filter_list) == 1:
            return filter_list[0]
    return None


def get_proper_url(list: List[str]):
    """
    First api request to host will be broken into multiple requests (by paths). All having sharing request id
    For ex: http://localhost:8080/apis/v1/specs/specId will become:
    1. http://localhost:8080/
    2. http://localhost:8080/apis/
    3. http://localhost:8080/apis/v1
    4. http://localhost:8080/apis/v1/specs
    They key is to capture appropriate url. And we will choose the longest one
    """
    count_max = -1
    proper_url = None
    for url in list:
        url_char_count = url.count()
        if url_char_count > count_max:
            count_max = url_char_count
            proper_url = url

    return proper_url


def get_http_archive(zap: ZAPv2, zap_message_id: str) -> str:
    """
    Get http archive(json) response given zap message id
    """
    msg_har = zap.core.message_har(zap_message_id)
    return msg_har


def get_request_id_header(header_arr):
    """
    Search and return request_id header value in array of request headers
    """
    request_id = None
    i = 0
    for header in header_arr:
        if "request_id" in header:
            break
        i = i + 1
    if (i + 1) < len(header_arr):
        request_id = header_arr[i + 1].split("\r\n")[0]
    return request_id


if __name__ == "__main__":
    zap = ZAPv2(apikey="ar5q06roaihvrek78jpp66mudj", proxies={"http": HOST})
    messages = get_messages(zap)
    get_urls(messages)
