import os
import sys
from pathlib import Path
from shared.envs import Environment
from dotenv import load_dotenv
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent


# EXTRA PATHS
# ----------------------------------------------------------------
LIST_PATH_TO_ADD = [

]
if LIST_PATH_TO_ADD:
    sys.path.extend(LIST_PATH_TO_ADD)

ENVS_DIR = BASE_DIR.parent / "envs"
ENV_BASE_FILE_PATH = ENVS_DIR / ".env.base"
load_dotenv(ENV_BASE_FILE_PATH)

ENVIRONMENT = os.environ.get("ENVIRONMENT")
logger.info(f"Environment project: {ENVIRONMENT}")
Environment.check_value(ENVIRONMENT)
env_enum = Environment(ENVIRONMENT)
ENV_FILE_PATH = ENVS_DIR / env_enum.get_file_name()
logger.info(f"File env: {ENV_FILE_PATH}")
#load_dotenv(ENV_FILE_PATH)