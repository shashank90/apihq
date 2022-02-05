from http.client import BAD_REQUEST
from pathlib import Path
from typing import List, Dict
import uuid
from urllib import request, response
from urllib.parse import parse_qs, urlsplit
from db.helper import update_run_details
from db.model.api_run import RunStatusEnum

# from body_parser import encode_multipart_formdata
from utils.constants import (
    DESCRIPTION,
    MESSAGE,
    REQUEST_ID,
    HAR_FOLDER,
    RESPONSE_VALIDATION,
    ISSUE_ID,
)
from tester.connectors.zap.factory import get_zap
from tester.connectors.zap.util import (
    get_http_archive,
    get_messages,
    get_url_detail,
    get_urls,
)
from werkzeug.datastructures import ImmutableMultiDict
from utils.file_handler import write_json
import os
from zapv2 import ZAPv2
from log.factory import Logger
from tester.modules.openapi.init_invoker import invoke_apis
from tester.modules.openapi.validator import request_validation, response_validation
from openapi_core.templating.paths.exceptions import PathError
from openapi_core.templating.responses.exceptions import ResponseFinderError
from openapi_core.validation.response.datatypes import ResponseValidationResult
from openapi_core.validation.request.datatypes import RequestValidationResult
from openapi_core.validation.exceptions import InvalidSecurity
from openapi_core.deserializing.exceptions import DeserializeError
from openapi_core import create_spec
from prance import ResolvingParser
from jsonschema import ValidationError
import json

logger = Logger(__name__)

ERROR_RESPONSE_VALIDATION_FILE = "errors_response_validation.json"
ERROR_REQUEST_VALIDATION_FILE = "errors_request_validation.json"
ISSUES_FILE = "issues.json"
REQUEST_METADATA_FILE = "request_metadata.json"
REQUEST_INTENT = "request_intent"
BAD_REQUEST = "BAD_REQUEST"
URL = "url"
OK = "200"


def get_har(zap: ZAPv2, zap_msg_id: str):
    """
    Get http archive response from zap given request_id
    """
    har_string = get_http_archive(zap, zap_msg_id)
    har_data = json.loads(har_string)
    return har_data


def _save_har(data_dir: str, request_id: str, har: Dict):
    """
    Save har(http archive) to file
    """
    har_file = request_id + ".json"
    har_dir = os.path.join(data_dir, HAR_FOLDER)
    # Create har file path along with dirs(if they don't exist)
    Path(har_dir).mkdir(parents=True, exist_ok=True)
    har_file_path = os.path.join(har_dir, har_file)
    write_json(har_file_path, har)


def save_har(data_dir: str, request_id: str, zap: ZAPv2, zap_msg_id: str) -> Dict:
    """
    Save http archive file got from zap for given request_id.
    Also returning har dict for further processing
    """
    har_data = get_har(zap, zap_msg_id)
    _save_har(data_dir, request_id, har_data)
    return har_data


def run(
    run_id: str, api_path: str, spec_path: str, data_dir: str, auth_headers: List[Dict]
):
    """
    Test API contract conformance by initiating requests that fall outside contract constraints
    """
    # Create and send payloads for each api
    logger.info(f"Running API Tests for api path: {api_path}")

    update_run_details(run_id, RunStatusEnum.IN_PROGRESS)

    (request_metadata_list, response_list) = invoke_apis(
        data_dir, api_path, spec_path, auth_headers
    )

    write_request_metadata(data_dir, request_metadata_list)

    openapi_core_spec = get_openapi_spec(spec_path)

    zap: ZAPv2 = get_zap()
    zap_messages = get_zap_messages(zap)

    # Validate each response against OpenAPI spec for each api
    response_validation_errors: List[str] = []
    request_validation_errors: List[str] = []
    issues: List[Dict] = []
    for response_object in response_list:

        # TODO: Construct these values from har data itself instead of getting from invoker
        full_api_path = response_object.get("full_api_path")
        path_params = response_object.get("path_params")
        response_status = response_object.get("response_status")

        # Get URL by matching request_id across messages captured via ZAP
        request_id = response_object.get(REQUEST_ID)
        url_detail = get_url_detl(request_id, zap_messages)
        zap_msg_id = url_detail.get("zap_message_id")
        har_data = save_har(data_dir, request_id, zap, zap_msg_id)

        # req_details: Dict = get_request_details(har_data)
        # req_details["path_params"] = path_params

        # Request validation errors. Record invalid requests that went through
        if response_status == OK:
            request_validation_errors.append({REQUEST_ID: request_id})

        # TODO: Investigate why openapi_core request validation is failing. See if master branch can be forked and changes made to convert bytes to string
        # req_error_messages = get_request_validation_errors(
        # full_api_path, openapi_core_spec, req_details
        # )

        # request_validations.append(
        # {REQUEST_ID: request_id, ERROR_MESSAGES: req_error_messages}
        # )

        # Response validation errors
        res_error_messages = get_response_validation_errors(
            full_api_path, openapi_core_spec, response_object
        )

        error: Dict = add_response_error(
            request_id, response_validation_errors, res_error_messages
        )

        # Add unique error to cumulative list of issues
        if error:
            issue_id = uuid.uuid4().hex
            error[ISSUE_ID] = issue_id
            issues.append(error)

    error_response_validation_file = os.path.join(
        data_dir, ERROR_RESPONSE_VALIDATION_FILE
    )

    error_request_validation_file = os.path.join(
        data_dir, ERROR_REQUEST_VALIDATION_FILE
    )

    issues_file = os.path.join(data_dir, ISSUES_FILE)

    # TODO: Save this to db (Add a request_id and connect table to requests table) so it can be joined with requests table
    write_json(error_response_validation_file, response_validation_errors)

    write_json(error_request_validation_file, request_validation_errors)

    write_json(issues_file, issues)

    # Update final db status
    update_run_details(run_id, RunStatusEnum.COMPLETED)


def add_response_error(
    request_id: str, response_validation_errors: List, res_error_messages: List
):
    """
    Add unique response errors
    """
    error: Dict = None
    if len(response_validation_errors) == 0:
        error: Dict = get_error(request_id, res_error_messages)
        response_validation_errors.append(error)

    elif is_error_new(response_validation_errors, res_error_messages):
        error: Dict = get_error(request_id, res_error_messages)
        response_validation_errors.append(error)

    return error


def get_error(request_id: str, error_messages: List[str]) -> Dict:
    """
    Return error object
    """
    return {
        REQUEST_ID: request_id,
        MESSAGE: error_messages,
        REQUEST_INTENT: BAD_REQUEST,
        DESCRIPTION: RESPONSE_VALIDATION,
    }


def is_error_new(response_validation_errors: List, res_error_messages: List):
    """
    Add only unique errors to final validation error list
    """
    total = len(res_error_messages)
    count = 0
    for m1 in res_error_messages:
        for m2 in response_validation_errors:
            for m3 in m2[MESSAGE]:
                if m1 == m3:
                    count = count + 1

    if count == total:
        return False
    return True


def write_request_metadata(data_dir: str, req_metadata: List[Dict]):
    """
    Write request validation errors to file.
    TODO Save this to db
    """
    request_metadata_file = os.path.join(data_dir, REQUEST_METADATA_FILE)
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


def get_url_detl(request_id: str, messages: List):
    """
    Get url details including zap_message_id given request_id (which binds request and response)
    """
    # messages = get_messages(zap)
    url_details = get_urls(messages)
    return get_url_detail(request_id, url_details)


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
    except ResponseFinderError as re:
        error_messages = get_error_messages(re)
    except Exception as e:
        error_messages = get_error_messages(e.schema_errors)

    logger.info(
        f"Validation response error messages {error_messages} for api path {full_api_path}"
    )

    return error_messages


def get_error_messages(schema_errors: List[ValidationError]):
    error_msgs = [schema_error.message for schema_error in schema_errors]
    return error_msgs
