from pathlib import Path
import base64
from urllib3._collections import HTTPHeaderDict
from typing import List, Dict
from backend.utils.file_handler import create_run_dir, get_run_dir_path, read_json
from urllib.parse import parse_qs, urlsplit
from backend.db.helper import update_run_details
from backend.db.model.api_run import RunStatusEnum
from backend.tester.connectors.zap.script_handler import enable_request_dump_script

# from body_parser import encode_multipart_formdata
from backend.utils.constants import (
    API_RUN_FAILED,
    CATEGORY,
    DEFAULT_REQUEST_ERROR_DESCRIPTION,
    DEFAULT_REQUEST_ERROR_SOLUTION,
    DEFAULT_RESPONSE_ERROR_DESCRIPTION,
    DEFAULT_RESPONSE_ERROR_SOLUTION,
    DESCRIPTION,
    ERROR_TYPE_REQUEST,
    ERROR_TYPE_RESPONSE,
    HTTP_CREATED,
    HTTP_OK,
    INSTANCES,
    ISSUE_TYPE,
    MESSAGE,
    REQUEST_ID,
    HAR_DIR,
    ISSUE_ID,
    SCHEMA_VALIDATION,
    SOLUTION,
    ZAP_MESSAGE_DIR,
    CONSTRAINT,
)
from backend.tester.connectors.zap.factory import get_zap
from backend.tester.connectors.zap.util import (
    get_http_archive,
    get_messages,
    get_zap_message_detail,
)
from werkzeug.datastructures import ImmutableMultiDict
from backend.utils.file_handler import write_json
import os
from zapv2 import ZAPv2
from backend.log.factory import Logger
from backend.tester.modules.openapi.init_invoker import invoke_apis
from backend.tester.modules.openapi.validator import (
    request_validation,
    response_validation,
)
from openapi_core.templating.paths.exceptions import PathError
from openapi_core.templating.responses.exceptions import ResponseFinderError
from openapi_core.templating.responses.exceptions import ResponseNotFound
from openapi_core.validation.response.datatypes import ResponseValidationResult
from openapi_core.validation.request.datatypes import RequestValidationResult
from openapi_core.validation.exceptions import InvalidSecurity
from openapi_core.deserializing.exceptions import DeserializeError
from openapi_core import create_spec
from prance import ResolvingParser
from jsonschema import ValidationError
import json
from backend.utils.uuid_handler import get_uuid

logger = Logger(__name__)

ERROR_RESPONSE_VALIDATION_FILE = "errors_response_validation.json"
ERROR_REQUEST_VALIDATION_FILE = "errors_request_validation.json"
ISSUES_FILE = "issues.json"
REQUESTS_FILE = "requests.json"
REQUEST_METADATA_FILE = "request_metadata.json"
REQUEST_INTENT = "request_intent"
BAD_REQUEST = "BAD_REQUEST"
URL = "url"


def get_har(zap: ZAPv2, zap_msg_id: str):
    """
    Get http archive response from zap given request_id
    """
    har_string = get_http_archive(zap, zap_msg_id)
    har_data = json.loads(har_string)
    return har_data


def _save_har(run_dir: str, request_id: str, har: Dict):
    """
    Save har(http archive) to file
    """
    har_file = request_id + ".json"
    har_dir = os.path.join(run_dir, HAR_DIR)
    # Create har file path along with dirs(if they don't exist)
    Path(har_dir).mkdir(parents=True, exist_ok=True)
    har_file_path = os.path.join(har_dir, har_file)
    write_json(har_file_path, har)


def save_har(run_dir: str, request_id: str, zap: ZAPv2, zap_msg_id: str) -> Dict:
    """
    Save http archive file got from zap for given request_id.
    Also returning har dict for further processing
    """
    har_data = get_har(zap, zap_msg_id)
    _save_har(run_dir, request_id, har_data)
    return har_data


def run(
    run_id: str, api_path: str, spec_path: str, data_dir: str, auth_headers: List[Dict]
):
    """
    Test API contract conformance by initiating requests that fall outside contract constraints
    """
    # Create and send payloads for each api
    logger.info(f"Running API Tests with run_id {run_id} for api path: {api_path}")

    # Create run dir and store request/response artifacts (post sdk generation here)
    run_dir = get_run_dir_path(data_dir, run_id)
    if not create_run_dir(run_dir):
        update_run_details(run_id, RunStatusEnum.ERROR, API_RUN_FAILED)
        return

    try:
        update_run_details(run_id, RunStatusEnum.IN_PROGRESS)

        # Enable ZAP request dump script
        enable_request_dump_script()

        # Continue overwriting sdk generation in case of multiple runs within data dir.
        # Only write requests & their results to separate run dirs
        (request_metadata, response_list) = invoke_apis(
            run_id, data_dir, run_dir, api_path, spec_path, auth_headers
        )

        write_request_metadata(run_dir, request_metadata)

        openapi_core_spec = get_openapi_spec(spec_path)

        zap: ZAPv2 = get_zap()

        # Get requests saved via our script
        zap_requests = get_zap_message_requests(run_dir)

        # Get messages proxied through zap
        # from_zap_messages = get_zap_messages(zap)

        # Validate each response against OpenAPI spec for each api
        response_validation_errors: List[str] = []
        request_validation_errors: List[str] = []
        requests = []
        issues: List[Dict] = []
        for response_object in response_list:

            full_api_path = response_object.get("full_api_path")
            # path_params = response_object.get("path_params")
            response_status = response_object.get("response_status")

            request_id = response_object.get(REQUEST_ID)
            zap_request = get_request_detail_from_zap_message(request_id, zap_requests)

            # request_detail = get_zap_message_details(
            #     request_id, zap_messages, from_zap_messages
            # )
            # zap_msg_id = request_detail.get("zap_message_id")
            # har_data = save_har(run_dir, request_id, zap, zap_msg_id)

            add_requests(request_id, zap_request, response_object, requests)

            # req_details: Dict = get_request_details(har_data)
            # req_details["path_params"] = path_params

            # Request validation errors. Record invalid requests that went through
            if response_status == HTTP_OK or response_status == HTTP_CREATED:
                add_request_error(
                    request_id, request_validation_errors, request_metadata, issues
                )

            # Response validation errors
            res_error_messages = get_response_validation_errors(
                full_api_path, openapi_core_spec, response_object
            )

            add_response_error(
                request_id, response_validation_errors, res_error_messages, issues
            )

        error_response_validation_file = os.path.join(
            run_dir, ERROR_RESPONSE_VALIDATION_FILE
        )

        error_request_validation_file = os.path.join(
            run_dir, ERROR_REQUEST_VALIDATION_FILE
        )

        # TODO: Save this to db (Add a request_id and connect table to requests table) so it can be joined with requests table
        write_json(error_response_validation_file, response_validation_errors)

        write_json(error_request_validation_file, request_validation_errors)

        requests_file = os.path.join(run_dir, REQUESTS_FILE)
        write_json(requests_file, requests)

        prepare_final_issues(
            request_validation_errors, response_validation_errors, issues
        )
        issues_file = os.path.join(run_dir, ISSUES_FILE)
        write_json(issues_file, issues)

        # Update final db status
        update_run_details(run_id, RunStatusEnum.COMPLETED)

    except Exception:
        logger.exception(f"Api Test Run failed to complete for run_id {run_id}")
        update_run_details(run_id, RunStatusEnum.ERROR, API_RUN_FAILED)


def add_requests(request_id: str, request: Dict, response: Dict, requests: List):
    """
    Parse zap har data and create request_response object
    """
    request_response = {}
    request_object = {}
    response_object = {}

    request_object["url"] = request.get("url")
    request_object["header"] = request.get("headers")
    request_object["body"] = request.get("body")

    response_object["status"] = response.get("response_status")
    response_object["header"] = serialize_headers(
        response.get("response_headers"), response.get("response_status")
    )
    response_object["body"] = extract_str(response.get("response_data"))

    request_response["request_id"] = request_id
    request_response["request"] = request_object
    request_response["response"] = response_object

    requests.append(request_response)


def serialize_headers(header_object: HTTPHeaderDict, status: str) -> str:
    """
    Serialize HttpHeaderDict
    """
    header_str = ""
    if header_object:
        for header_name in header_object.keys():
            header_str = (
                header_str
                + header_name
                + ":"
                + ",".join(header_object.getheaders(header_name))
                + "\n"
            )

    # Append status to headers
    if status:
        header_str = header_str + "Status" + ":" + str(status) + "\n"

    return header_str


def get_from_har(har_data: Dict):
    """
    Form request and response objects from har files
    """
    request_object = {}
    response_object = {}

    if "log" in har_data:
        log = har_data["log"]
        if "entries" in log and len(log["entries"]) > 0:
            entry = log["entries"][0]
            if "request" in entry:
                request = entry["request"]
                url = request["url"]
                request_object["url"] = url

                if "headers" in request:
                    headers = request["headers"]
                    request_object["header"] = form_headers(headers)
                if "postData" in request:
                    body = request["postData"]
                    if "text" in body:
                        request_object["body"] = body["text"]
            if "response" in entry:
                response = entry["response"]
                if "status" in response:
                    response_object["status"] = response["status"]
                if "headers" in response:
                    headers = response["headers"]
                    response_object["header"] = form_headers(
                        headers, status=response.get("status")
                    )
                if "content" in response:
                    content = response["content"]
                    if "text" in content:
                        b64decoded = base64.b64decode(content["text"])
                        response_object["body"] = extract_str(b64decoded)

        return request_object, response_object


def extract_str(content):
    """
    Extract text from bytes-like object, if it is one or just return the str
    """
    string: str = ""
    try:
        string = content.decode("utf-8")
    except UnicodeDecodeError:
        logger.warning("Given content isn't a bytes-like object")
        string = content
    except Exception as e:
        string = content

    return string


def form_headers(headers: List[Dict], status: str = None):
    """
    Create header string from list of header name/value pair
    """
    header_str = ""
    for header in headers:
        header_str = header_str + header["name"] + ":" + header["value"] + "\n"

    # Append status to headers
    if status:
        header_str = header_str + "Status" + ":" + str(status) + "\n"

    return header_str


def add_response_error(
    request_id: str,
    response_validation_errors: List,
    res_error_messages: List,
    issues: List[Dict],
):
    """
    Add response errors
    """
    error: Dict = None

    error: Dict = get_error(
        request_id,
        res_error_messages,
        ERROR_TYPE_RESPONSE,
        DEFAULT_RESPONSE_ERROR_DESCRIPTION,
        DEFAULT_RESPONSE_ERROR_SOLUTION,
        SCHEMA_VALIDATION,
    )

    if len(response_validation_errors) == 0:
        response_validation_errors.append(error)
    else:
        existing_error = get_response_error(
            response_validation_errors, res_error_messages
        )
        if existing_error:
            instances = existing_error.get(INSTANCES)
            instances.append(request_id)
        else:
            response_validation_errors.append(error)


def add_request_error(
    request_id: str,
    request_validation_errors: List,
    request_metadata: List[Dict],
    issues: List[Dict],
):
    req_details = get_request_metadata(request_id, request_metadata)

    messages = [req_details.get("message")]

    category = req_details.get(CONSTRAINT)
    error: Dict = get_error(
        request_id,
        messages,
        ERROR_TYPE_REQUEST,
        DEFAULT_REQUEST_ERROR_DESCRIPTION,
        DEFAULT_REQUEST_ERROR_SOLUTION,
        category,
    )

    if len(request_validation_errors) == 0:
        request_validation_errors.append(error)
    else:
        existing_error = get_request_error(request_validation_errors, category)
        if existing_error:
            instances = existing_error.get(INSTANCES)
            instances.append(request_id)
        else:
            request_validation_errors.append(error)


def get_error(
    request_id: str,
    error_messages: List[str],
    issue_type: str,
    description: str,
    solution: str,
    category: str = None,
) -> Dict:
    """
    Return error object
    """
    return {
        REQUEST_ID: request_id,
        MESSAGE: error_messages,
        REQUEST_INTENT: BAD_REQUEST,
        ISSUE_TYPE: issue_type,
        DESCRIPTION: description,
        SOLUTION: solution,
        CATEGORY: category,
        INSTANCES: [request_id],
    }


def prepare_final_issues(
    request_errors: List[Dict], response_errors: List[Dict], final_issues: List[Dict]
):
    """
    Add up all issues(request, response) in that order
    """
    # Add request errors
    for error in request_errors:
        add_issue(error, final_issues)

    # Add response errors
    for error in response_errors:
        add_issue(error, final_issues)


def add_issue(error: Dict, final_issues: List[Dict]):
    """
    Add error to cumulative list of issues
    """
    # Add unique error to cumulative list of issues
    if error:
        issue_id = get_uuid()
        error[ISSUE_ID] = issue_id
        final_issues.append(error)


def get_request_metadata(request_id: str, request_metadata: List[Dict]):
    """
    Get request metadata for given request_id
    """
    for item in request_metadata:
        if request_id == item["request_id"]:
            return item


def get_request_error(validation_errors: List, category: str):
    """
    Retain one error per constraint category and add the rest to instances
    """
    for error in validation_errors:
        if category == error.get(CATEGORY):
            return error
    return None


def get_response_error(validation_errors: List, error_messages: List):
    """
    Add only unique errors to final validation error list. Return existing error in case of match else None
    """
    error_match: Dict = None
    total = len(error_messages)
    for m1 in validation_errors:
        count = 0
        error_match = m1
        for m2 in error_messages:
            for m3 in m1[MESSAGE]:
                if m2 == m3:
                    count = count + 1

        if count == total:
            return error_match
    return None


def write_request_metadata(run_dir: str, req_metadata: List[Dict]):
    """
    Write request validation errors to file.
    TODO Save this to db
    """
    request_metadata_file = os.path.join(run_dir, REQUEST_METADATA_FILE)
    write_json(request_metadata_file, req_metadata)
    if os.path.exists(request_metadata_file):
        logger.info(
            f"Hey wrote request metadata file {request_metadata_file}. Check it out"
        )


def get_zap_messages(zap: ZAPv2):
    """
    Get all messages proxied through ZAP
    """
    messages = get_messages(zap)
    return messages


# def get_zap_message_details(
#     request_id: str, zap_request_messages: List[Dict], from_zap_messages: List[Dict]
# ):
#     """
#     Get url details including zap_message_id given request_id
#     """
#     url_request_id = get_url_from_zap_message(request_id, zap_request_messages)
#     url = url_request_id.get("url")
#     return get_zap_message_detail(request_id, url, from_zap_messages)


def get_request_detail_from_zap_message(
    request_id: str, zap_request_messages: List[Dict]
):
    """
    Extract request details from list of saved(via dump request script) ZAP messages
    """
    filtered: List = filter(
        lambda x: x["request_id"] == request_id, zap_request_messages
    )
    if filtered:
        filter_list = list(filtered)
        if len(filter_list) == 1:
            return filter_list[0]
    return None


def get_zap_message_requests(run_dir: str):
    """
    Get zap message ids by reading file names
    """
    zap_msg_dir = os.path.join(run_dir, ZAP_MESSAGE_DIR)

    # Form list of request_id and zap_message_id
    items = []
    for file_item in os.listdir(zap_msg_dir):
        temp = file_item.split("_")
        request_id = temp[0]
        file_item_path = os.path.join(zap_msg_dir, file_item)
        data = read_json(file_item_path)
        url = data.get("url")
        headers = data.get("headers")
        body = data.get("body")
        items.append(
            {"request_id": request_id, "url": url, "headers": headers, "body": body}
        )
    return items


def get_openapi_spec(spec_path: str):
    """
    Get openapi in dict form
    """
    parser = ResolvingParser(spec_path)
    spec = parser.specification
    return create_spec(spec)


def get_request_details(har_data: Dict):
    """
    Extract headers, query_params, body from har object
    """
    req_detail = {}
    entries = har_data.get("log").get("entries")
    if entries and len(entries) > 0:
        entry = entries[0]
        request = entry.get("request")
        headers = request.get("headers")
        http_method = request.get("method").lower()
        req_detail["http_method"] = http_method

        # Flatten list of dicts to single dict
        req_detail["headers"] = {k: v for i in headers for k, v in i.items()}

        # Get query params from url. Try 'queryString' node also
        url = request.get("url")
        query = urlsplit(url).query
        params = parse_qs(query)
        query_params: Dict = {k: v[0] for k, v in params.items()}
        # Convert this to werkzeug ImmutableMultiDict as openapi_core OpenAPIRequest object expects this data type
        req_detail["query_params"] = ImmutableMultiDict(query_params)

        # Get post data
        post_data = request.get("postData")
        if post_data:
            mimetype = post_data.get("mimeType").split(";")[0]
            req_detail["mimetype"] = mimetype

            body_text = post_data.get("text")
            # TODO: Convert http multipart/form-data to email multipart/form-data
            req_detail["body"] = get_email_mime_multipart_form_data()

    return req_detail


def get_email_mime_multipart_form_data():
    """
    openapi_core expects multipart/form-data to be encoded using email multipart/form-data for further processing.
    Hence adding translation layer to convert http multipart/form-data to email multipart/form-data
    """
    pass
    # return encode_multipart_formdata(
    #     [
    #         {
    #             "collectionName": "valid",
    #             "contentType": "text/plain",
    #         },
    #         {
    #             "file": "",
    #             "contentType": "text/plain",
    #             "filename": "eff00875-7828-11ec-a821-1181c30f7749.txt",
    #         },
    #     ]
    # )


def get_request_validation_errors(full_api_path: str, spec: Dict, req_details: Dict):

    request_validation_results: RequestValidationResult = request_validation(
        full_api_path, spec, req_details
    )

    error_messages: List[ValidationError] = []

    try:
        request_validation_results.raise_for_errors()
    except PathError as pe:
        error_messages = get_error_messages(pe)
    except InvalidSecurity as ie:
        error_messages = str(ie)
    except DeserializeError as de:
        # Deserialization of multipart/form-data relies on email.parser,
        # which requires further translation from http multipart/form-data body.
        # Hence perform your own deserialization for this mimetype
        pass
    except Exception as e:
        error_messages = get_error_messages(e.schema_errors)

    logger.info(
        f"Validation request error messages {error_messages} for api path {full_api_path}"
    )

    return error_messages


def get_response_validation_errors(
    full_api_path: str, spec: Dict, response_object: Dict
):

    response_validation_results: ResponseValidationResult = response_validation(
        spec, response_object
    )

    error_messages: List[ValidationError] = []

    try:
        response_validation_results.raise_for_errors()
    except PathError as pe:
        error_messages = get_error_messages(pe)
    except ResponseNotFound as rn:
        logger.info(str(rn))
        error_messages.append(str(rn))
    except ResponseFinderError as re:
        error_messages = get_error_messages(re)
    except Exception as e:
        error_messages = get_error_messages(e.schema_errors)

    logger.info(
        f"Validation response error messages {error_messages} for api path {full_api_path}"
    )

    return error_messages


# TODO: Deal with response not found (500)? ResponseNotFound is not a list
def get_error_messages(schema_errors: List[ValidationError]):
    error_msgs = [schema_error.message for schema_error in schema_errors]
    return error_msgs
