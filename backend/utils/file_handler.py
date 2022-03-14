import json
import os
import shutil
import threading
from pathlib import Path
from typing import Dict, List

from backend.log.factory import Logger
from backend.utils.constants import DATA_DIR_PREFIX, RUN, WORK_DIR

logger = Logger(__name__)


def create_spec_folder(spec_id: str) -> str:
    data_dir = None
    try:
        data_dir = os.path.join(WORK_DIR, DATA_DIR_PREFIX + spec_id)
        logger.info(f"Creating API spec dir {data_dir}...")
        Path(data_dir).mkdir(exist_ok=True)
    except OSError as e:
        logger.error(e)
    return data_dir


def create_run_dir(run_dir: str) -> bool:
    """
    Create run dir within data_dir for given run id
    """
    try:
        Path(run_dir).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Could not create run dir {run_dir}. Error: {str(e)}")
    return False


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


def get_run_dir_path(data_dir: str, run_id: str):
    return os.path.join(data_dir, RUN, run_id)


def get_file_name_and_extension(file_name):
    """
    Extract file name and extension from file name. Ex: (abc.yaml) -> abc & yaml
    """
    filename, file_extension = os.path.splitext(file_name)
    return (filename, file_extension)


def read_file_into_list(file_path) -> List[str]:
    """
    Read file contents into list of strings
    """
    str_list = []
    with open(file_path) as my_file:
        for line in my_file:
            str_list.append(line.rstrip("\n"))
    return str_list
