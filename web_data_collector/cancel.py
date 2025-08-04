# remote imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json

# local imports
from utils.config_logger import setup_logger, log_with_context
from utils.get_info import get_yesterday_date, get_penultimate_date
from config.settings import DATA_PATHS, TEMP_DIR, LINKS, ELEMENTS
from utils.reader import wait_download_csv
from utils.browser_setup import create_authenticated_driver

# %(name)s <<< module name
logger = setup_logger(__name__)

# global support variables
star_date = get_penultimate_date(DATA_PATHS['gold']['cancel'], 'data_criterio') # <<< penultimate update date in the gold/olpn folder
end_date = get_yesterday_date() # <<< current date entered in the final data field
control_dir = TEMP_DIR['BRONZE']['cancel'] # <<< folder monitored by the "wait_download_csv" function

@log_with_context(job='data_extraction_cancel', logger=logger)
def data_extraction_cancel(cookies: list[dict], dowload_dir: Path) -> None:

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
        driver.get(LINKS['LOGIN_CANCEL'])

        logger.info('site acessado com sucesso', extra={
            'job': 'data_extraction_cancel',
            'status': 'sucess'
        })

        # verificando se o frame esta disponivel e acessando
        if not wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, ELEMENTS['frame']))):
            logger.error('erro ao acesso o frame', extra={
                'job': 'data_extraction_cancel',
                'status': 'failure'
            })

        logger.info('iniciando preenchimento de formulario cancel', extra={
            'job': 'data_extraction_cancel',
            'status': 'starde'
        })

        filial = wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENTS['ELEMENTS_CANCEL']['element_filial_id'])
        ))
        if filial:
            Select(filial).select_by_value(ELEMENTS['ELEMENTS_CANCEL']['element_filial'])

        dt_start = wait.until(EC.element_to_be_clickable(
             (By.ID, ELEMENTS['ELEMENTS_CANCEL']['element_dt_start']))
        )
        if dt_start:
             dt_start.clear()
             dt_start.send_keys(star_date)

        dt_end = wait.until(EC.element_to_be_clickable(
             (By.ID, ELEMENTS['ELEMENTS_CANCEL']['element_dt_end']))
        )
        if dt_end:
             dt_end.clear()
             dt_end.send_keys(end_date)

        confirmar = wait.until(EC.element_to_be_clickable(
             (By.ID, ELEMENTS['ELEMENTS_CANCEL']['element_confirm'])
        ))
        if confirmar:
             confirmar.click()
             logger.info('formulario cancel preenchido com sucesso, iniciando downlo', extra={
                  'job': 'data_extraction_cancel',
                  'status': 'sucess'
             })

        if wait_download_csv(dir=control_dir):
            logger.info('download do arquivo cancel concluido', extra={
                'job': 'data_extraction_cancel',
                'status': 'sucess'
            })
        else:
            logger.critical('download do arquivo cancel falhou', extra={
                'job': 'data_extraction_cancel',
                'status': 'failure'
            })

    except Exception as e:
        logger.exception(f'erro ao extrair dados do cancel: {e}', extra={
            'job': 'data_extraction_cancel',
            'status': 'failure'
        })

    finally:
            driver.quit()

def data_extraction_cancel_from_file(cookies_path: str, download_dir: Path) -> None:
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    data_extraction_cancel(cookies, download_dir)