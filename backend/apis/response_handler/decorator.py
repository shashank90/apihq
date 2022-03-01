from backend.utils.constants import (
    ERROR,
    GENERIC_ERROR_MESSAGE,
    HTTP_INTERNAL_SERVER_ERROR,
    INTERNAL_SERVER_ERROR,
)
from functools import wraps
from backend.apis.model.http_error import HttpResponse
from flask import jsonify
from backend.log.factory import Logger


logger = Logger(__name__)


def handle_response(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        # handle different types of errors and return messages accordingly with status code
        except Exception as e:
            if isinstance(e, HttpResponse):
                if e.type == ERROR:
                    error_obj = get_error_object(e.message, e.code)
                    return (
                        jsonify(error_obj),
                        e.http_status,
                    )
                else:
                    return (
                        jsonify({"message": e.message, "code": e.code}),
                        e.http_status,
                    )
            else:
                logger.error(str(e))
                message = GENERIC_ERROR_MESSAGE
                code = INTERNAL_SERVER_ERROR
                error_obj = get_error_object(message, code)
                return (
                    jsonify(error_obj),
                    HTTP_INTERNAL_SERVER_ERROR,
                )

    return wrapped


def get_error_object(message, code):
    return {
        "error": {
            "message": message,
            "code": code,
        }
    }
