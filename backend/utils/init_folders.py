from genericpath import exists
from pathlib import Path
from backend.utils.constants import LOG_DIR

# from log.factory import Logger

# logger = Logger(__name__)


def create_folders():
    """
    Create folders needed during app runtime
    """
    print("Creating folders needed at app runtime...")
    # Create LOG dir(folder that stores application logs and data dirs)
    Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
