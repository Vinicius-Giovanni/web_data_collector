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
    TEMP_DIR = Path('/mnt/bronze/TEMP_DIR_CHROME/web_data_collector')
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
    LOG_DIR = Path(r'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Gold (Business Layer)/logs')

    # path for .env file
    ENV_PATH = Path(r'C:/Users/2960006959/Desktop/project\web_data_collector/config/.env')

    # path for base data
    BASE_PATH = Path(r'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse')
    
    # data paths temporary for chrome
    TEMP_DIR = Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector')

    # all data paths
    DATA_PATHS = {
        'bronze': {
            'olpn' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '3.11 - Status Wave + oLPN')
        },
        'silver': {
            'olpn' : Path(BASE_PATH / 'Silver (Business Layer)' / '3.11 - Status Wave + oLPN')
        },
        'gold': {
            'olpn' : Path(BASE_PATH / 'Gold (Business Layer)' / '3.11 - Status Wave + oLPN')
        }
    }

    LINKS = {
        'LOGIN_CSI': 'https://viavp-sci.sce.manh.com/bi/?perspective=home',
        'LOGIN_OLPN' : 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=i79E326D8D72B45F795E0897FCE0606F6&objRef=i79E326D8D72B45F795E0897FCE0606F6&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22i79E326D8D72B45F795E0897FCE0606F6%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%223.11%20-%20Status%20Wave%20%2B%20oLPN%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D'
    }




LOG_PATH = LOG_DIR / Path(r'log_web_data_collector.log')

load_dotenv(dotenv_path=ENV_PATH)