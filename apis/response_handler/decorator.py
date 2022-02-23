from utils.constants import ERROR, GENERIC_ERROR_MESSAGE, INTERNAL_SERVER_ERROR
from functools import wraps
from apis.model.http_error import HttpResponse
from flask import jsonify
from log.factory import Logger


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
                    return (
                        jsonify({"error": {"message": e.message, "code": e.code}}),
                        e.http_status,
                    )
                else:
                    return (
                        jsonify({"message": e.message, "code": e.code}),
                        e.http_status,
                    )
            else:
                logger.error(str(e))
                return (
                    jsonify(
                        {
                            "message": GENERIC_ERROR_MESSAGE,
                            "code": INTERNAL_SERVER_ERROR,
                        }
                    ),
                    500,
                )

    return wrapped
