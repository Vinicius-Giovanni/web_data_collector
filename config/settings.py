from pathlib import Path
from dotenv import load_dotenv
import os

# detects if it is running inside the docker container
IS_DOCKER = os.environ.get("IS_DOCKER", "0") == "1"

if IS_DOCKER:

    LOCATE = 'docker'

    # paths for linux container
    LOG_FILE = Path('/mnt/gold/logs')
    ENV_PATH = Path('/web_data_collector/config/.env')

else:

    LOCATE = 'windows'
    
    # paths for windows container
    LOG_FILE = Path(r'C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\Sala PCP - Online_A.B.S - Data Lakehouse\Gold (Business Layer)\logs')
    ENV_PATH = Path(r'C:\Users\2960006959\Desktop\project\web_data_collector\config\.env')

LOG_PATH = LOG_FILE / Path(r'log_web_data_collector.log')

load_dotenv(dotenv_path=ENV_PATH)