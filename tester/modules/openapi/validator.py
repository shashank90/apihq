from typing import Dict
from urllib.parse import urljoin
from openapi_core.validation.response.datatypes import OpenAPIResponse
from openapi_core.validation.request.datatypes import OpenAPIRequest
from openapi_core.validation.response.datatypes import ResponseValidationResult
from openapi_core.validation.request.datatypes import RequestParameters
from openapi_core.validation.response.validators import ResponseValidator
from werkzeug.datastructures import Headers
from openapi_core.validation.request.validators import RequestValidator


def get_openapi_request(
    full_url_pattern,
    method,
    mimetype,
    query_params=None,
    path_params=None,
    headers=None,
    body=None,
    cookies=None,
):

    header = Headers(headers)
    parameters = RequestParameters(
        path=path_params,
        query=query_params,
        header=header,
        cookie=cookies,
    )
    return OpenAPIRequest(
        full_url_pattern=full_url_pattern,
        method=method,
        parameters=parameters,
        body=body,
        mimetype=mimetype,
    )


def request_validation(full_api_path: str, spec: Dict, req_details: Dict):
    validator = RequestValidator(spec)

    http_method = req_details.get("http_method")
    mimetype = req_details.get("mimetype")
    path_params = req_details.get("path_params")
    query_params = req_details.get("query_params")
    headers = req_details.get("headers")
    body_txt = req_details.get("body")
    # body_bytes = body_txt.encode("ASCII")
    # print("Body bytes!!!!!")
    # print(body_bytes)

    openapi_request = get_openapi_request(
        full_api_path,
        http_method,
        mimetype,
        query_params=query_params,
        path_params=path_params,
        headers=headers,
        body=body_txt,
    )
    return validator.validate(openapi_request)


def response_validation(spec: Dict, response_object: Dict) -> ResponseValidationResult:
    """
    Validate response against OpenAPI spec using openapi-core package
    """
    url = response_object.get("full_api_path")
    http_method = response_object.get("http_method")
    mimetype = response_object.get("mimetype")
    response_data = response_object.get("response_data")
    response_status = response_object.get("response_status")

    openapi_response = OpenAPIResponse(
        data=response_data,
        status_code=response_status,
        mimetype=mimetype,
    )

    openapi_request = get_openapi_request(url, http_method, mimetype)

    validator = ResponseValidator(spec)

    return validator.validate(openapi_request, openapi_response)
