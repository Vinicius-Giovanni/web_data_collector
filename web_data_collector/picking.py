# remote imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

# local imports
from utils.config_logger import setup_logger, log_with_context
from utils.get_info import get_yesterday_date, get_penultimate_date
from config.settings import DATA_PATHS, TEMP_DIR, LINKS, ELEMENTS
from utils.reader import wait_download_csv
from utils.browser_setup import create_authenticated_driver

# %(name)s <<< module name
logger = setup_logger(__name__)

# global support variables
star_date = get_penultimate_date(DATA_PATHS['gold']['picking'], 'data_criterio') # <<< penultimate update date in the gold/olpn folder
end_date = get_yesterday_date() # <<< current date entered in the final data field
control_dir = TEMP_DIR['BRONZE']['picking'] # <<< folder monitored by the "wait_download_csv" function

@log_with_context(job='data_extraction_picking', logger=logger)
def data_extraction_picking(cookies: list[dict], dowload_dir: Path) -> None:

    #* Creation of the module responsible for assuming the driver of the 'login_csi' function and extracting a .csv file from the system

    #*  Module flow:
    #* - receives as parameter the 'driver' of the 'login_csi' function 
    #* - .csv file extraction 
    #* - call to the "wait_download_csv" function that monitors the directory configured by the "init_browser" function 
    #* - call of the specific pipeline for the downloaded file, according to its name 
    #*   - according to the file name, it will activate the specific pipeline for it, the pipeline will receive as a parameter the path of the downloaded file
    #* - transform the .csv file into .parquet in the directory synchronized with sharepoint 

    driver = create_authenticated_driver(cookies, download_dir=dowload_dir)

    try:
        wait = WebDriverWait(driver, 30)
        driver.get(LINKS['LOGIN_PICKING'])

        logger.info('site acessado com sucesso', extra={
            'job': 'data_extraction_picking',
            'status': 'success'
        })