from pathlib import Path
from dotenv import load_dotenv
import os

# detects if it is running inside the docker container
IS_DOCKER = os.environ.get("IS_DOCKER", "0") == "1"

if IS_DOCKER:

    LOCATE = 'docker'

    # paths for linux container
    LOG_DIR = Path('/mnt/gold/logs')
    ENV_PATH = Path('/web_data_collector/config/.env')
    BASE_PATH = Path('/mnt')
    DATA_PATHS = {
        'bronze': {
            'status_olpn' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '3.11 - Status Wave + oLPN')
        },
        'silver': {
            'status_olpn' : Path(BASE_PATH / 'Silver (Business Layer)' / '3.11 - Status Wave + oLPN')
        },
        'gold': {
            'status_olpn' : Path(BASE_PATH / 'Gold (Business Layer)' / '3.11 - Status Wave + oLPN')
        }
    }

else:

    LOCATE = 'windows'
    
    # --- paths for windows container ---

    # path for logs
    LOG_DIR = Path(r'C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\Sala PCP - Online_A.B.S - Data Lakehouse\Gold (Business Layer)\logs')

    # path for .env file
    ENV_PATH = Path(r'C:\Users\2960006959\Desktop\project\web_data_collector\config\.env')

    # path for base data
    BASE_PATH = Path(r'C:\Users\2960006959\OneDrive - Grupo Casas Bahia S.A\Sala PCP - Online_A.B.S - Data Lakehouse')

    DATA_PATHS = {
        'bronze': {
            'status_olpn' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '3.11 - Status Wave + oLPN')
        },
        'silver': {
            'status_olpn' : Path(BASE_PATH / 'Silver (Business Layer)' / '3.11 - Status Wave + oLPN')
        },
        'gold': {
            'status_olpn' : Path(BASE_PATH / 'Gold (Business Layer)' / '3.11 - Status Wave + oLPN')
        }
    }




LOG_PATH = LOG_DIR / Path(r'log_web_data_collector.log')

load_dotenv(dotenv_path=ENV_PATH)