import os
from backend.utils.constants import (
    DEFAULT_POSTMAN_ERROR_MESSAGE,
    POSTMAN_ERROR_MESSAGE_PREFIX,
)
from backend.utils.file_handler import get_file_name_and_extension
from backend.utils.os_cmd_runner import run_cmd
from backend.log.factory import Logger

logger = Logger(__name__)


def get_remote_addr(request):
    """
    Get remote ip address from request object
    """
    return request.environ.get("HTTP_X_REAL_IP", request.remote_addr)


def convert_postman_collection(
    user_id: str, data_dir: str, file_name: str, collection_file_path: str
):
    """
    Utility to convert postman collection to openapi yaml
    """
    logger.info(
        f"Converting Postman collection: [{collection_file_path}] for user: [{user_id}]"
    )
    openapi_file_path = None
    updated_file_name = None
    error_message = None

    # Extract filename and extension from given filename(ex: collection.json)
    filename, _ = get_file_name_and_extension(file_name)

    updated_file_name = filename + ".yaml"
    openapi_file_path = os.path.join(data_dir, updated_file_name)

    output = None
    try:
        output, run_error = run_cmd(
            ["p2o", collection_file_path, "-f", openapi_file_path],
            timeout=50,
        )
        if run_error:
            error_message = POSTMAN_ERROR_MESSAGE_PREFIX + run_error
        logger.debug(f"Postman collection to openapi conversion output: {output}")
    except Exception as e:
        logger.error(
            f"Could not convert Postman collection to openapi. Error: {str(e)}"
        )
        error_message = POSTMAN_ERROR_MESSAGE_PREFIX + DEFAULT_POSTMAN_ERROR_MESSAGE

    return openapi_file_path, updated_file_name, error_message
