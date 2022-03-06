import logging
import os
from datetime import datetime

from backend.utils.constants import LOG_FILE_NAME, LOG_DIR
from inspect import currentframe, getframeinfo

# Rotating File Handler:
# file_handler = logging.handlers.RotatingFileHandler(
#     log_file, maxBytes=(1048576 * 5), backupCount=7
# )


def get_file_name():
    return datetime.now().strftime(LOG_FILE_NAME + "_%H_%M_%d_%m_%Y.log")


def init_logger():
    file_name = get_file_name()
    log_file = os.path.join(LOG_DIR, file_name)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(threadName)s] [%(levelname)s] [%(name)s:%(lineno)s] %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


class Logger:
    def __init__(self, name):
        self.name = name

    # Hack to include txn_id. Need an elegant solution to include arbitrary keys
    def info(self, msg: str, **kwargs):
        logging.getLogger(self.name).info(msg)

    # Hack to include txn_id. Need an elegant solution to include arbitrary keys
    def exception(self, msg: str, **kwargs):
        logging.getLogger(self.name).exception(msg)

    def error(self, msg: str, **kwargs):
        logging.getLogger(self.name).error(msg)

    def warning(self, msg: str, **kwargs):
        logging.getLogger(self.name).warning(msg)

    def debug(self, msg: str, **kwargs):
        logging.getLogger(self.name).debug(msg)
