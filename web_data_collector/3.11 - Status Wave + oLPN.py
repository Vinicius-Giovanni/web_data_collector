# remote imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

# local imports
from utils.config_logger import setup_logger
from utils.get_info import get_yesterday_date, get_penultimate_date

# %(name)s <<< module name
logger = setup_logger(__name__)

star_date = get_penultimate_date(parquet_folder=)
end_date = get_yesterday_date(format='%d/%m/%Y')