import json
import os
import shutil
import threading
from pathlib import Path
from typing import Dict

from log.factory import Logger
from utils.constants import DATA_DIR_PREFIX, DISCOVERED_DIR, data_dir, WORK_DIR

logger = Logger(__name__)

# Example of shared global variable

# class DataDirCounter(object):
# def __init__(self, val=0):
# self.lock = threading.Lock()
# self.counter = val
#
# def increment(self):
# print("Waiting for a lock...")
# self.lock.acquire()
# try:
# print("Acquired a lock, counter value: ", self.counter)
# self.counter = self.counter + 1
# finally:
# print("Released a lock, counter value: ", self.counter)
# self.lock.release()
#
# def get_counter(self):
# return self.counter
#
#
# Shared Global Variable
# data_dir_counter = DataDirCounter()


def create_spec_folder(spec_id: str) -> str:
    data_dir = None
    try:
        data_dir = os.path.join(WORK_DIR, DATA_DIR_PREFIX + spec_id)
        logger.info(f"Creating API spec dir {data_dir}...")
        Path(data_dir).mkdir(exist_ok=True)
    except OSError as e:
        logger.error(e)
    return data_dir


def remove_files(folder: str):
    logger.info(f"Removing files from folder {folder}")
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception:
            logger.exception(f"Failed to delete {file_path}")


def write_json(file_path: str, dicT: Dict):
    """
    Dump dict to json file
    """
    with open(file_path, "w") as fp:
        json.dump(dicT, fp)


def read_content(file_path: str) -> str:
    """
    Read all contents of a file into a string
    """
    content = None
    if os.path.exists(file_path):
        with open(file_path) as f:
            content = f.read()
    return content


def read_json(file_path: str) -> Dict:
    """
    Read json file contents into dict
    """
    result = None
    with open(file_path, "r") as fh:
        result = json.load(fh)
    return result


def write_content(file_name: str, content: str):
    """
    Dump string content to file
    """
    with open(file_name, "w+", encoding="utf-8") as f:
        f.write(content)


def is_file_exists(path):
    file_path = Path(path)
    if file_path.is_file():
        return True
    return False
