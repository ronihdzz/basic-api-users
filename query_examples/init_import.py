import os
import sys
from pathlib import Path
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
logger.info(f"BASE_DIR: {BASE_DIR}")

# EXTRA PATHS
# -----------------------------------------------------------------

PATH_ROOT = os.path.join(BASE_DIR)
PATH_SRC = os.path.join(PATH_ROOT, "src")
LIST_PATHS = [PATH_ROOT, PATH_SRC]
logger.info(f"LIST_PATHS: {LIST_PATHS}")

# IMPORT
# -----------------------------------------------------------------

for path in LIST_PATHS:
    if path not in sys.path:
        sys.path.append(path)
        logger.info(f"Added path: {path}")
