# remote imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json

# local imports
from utils.config_logger import setup_logger, log_with_context
from config.settings import TEMP_DIR, LINKS, ELEMENTS
from utils.reader import wait_download_csv
from utils.browser_setup import create_authenticated_driver
from web_data_collector.login import chamada_funcao_dates, yesterday_date

# %(name)s <<< module name
logger = setup_logger(__name__)

# global support variables
star_date = chamada_funcao_dates # <<< penultimate update date in the gold/olpn folder
end_date = yesterday_date # <<< current date entered in the final data field

@log_with_context(job='data_extraction_olpn', logger=logger)
def data_extraction_olpn(cookies: list[dict], dowload_dir: Path) -> None:

    control_dir = dowload_dir

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
        driver.get(LINKS['LOGIN_OLPN'])

        logger.info('site acessado com sucesso', extra={
            'job': 'data_extraction_olpn',
            'status': 'success'
        })

        # verificando se o frame esta disponivel e acessando
        if not wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, ELEMENTS['frame']))):
            logger.error('erro ao acessar o frame', extra={
                'job': 'data_extraction_olpn',
                'status': 'failure'
            })
        
        # verificando se o elemento de titulo esta disponivel
        if not wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, ELEMENTS['ELEMENTS_OLPN']['element_title']))):
            logger.error('erro ao localizar o elemento de titulo', extra={
                'job': 'data_extraction_olpn',
                'status': 'failure'
            })
        
        logger.info('inicinado preenchimento de formulario olpn', extra={
            'job': 'data_extraction_olpn',
            'status': 'started'
        })

        filial = wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENTS['ELEMENTS_OLPN']['element_filial_id']))
        )
        if filial:
            Select(filial).select_by_value(ELEMENTS['ELEMENTS_OLPN']['element_filial'])

        dt_start = wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENTS['ELEMENTS_OLPN']['element_dt_start']))
        )
        if dt_start:
            dt_start.clear()
            dt_start.send_keys(star_date)

        dt_end = wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENTS['ELEMENTS_OLPN']['element_dt_end']))
        )
        if dt_end:
            dt_end.clear()
            dt_end.send_keys(end_date)

        # selecionando os itens do listbox
        if wait.until(EC.visibility_of_element_located(
            (By.XPATH, ELEMENTS['ELEMENTS_OLPN']['element_listbox']))):

            itens = driver.find_elements(By.XPATH, ELEMENTS['ELEMENTS_OLPN']['elements_listbox'])

            for item in itens:
                nome = item.get_attribute(ELEMENTS['ELEMENTS_OLPN']['element_get_item'])
                if nome in ELEMENTS['ELEMENTS_OLPN']['list_itens']:
                    is_checked = item.get_attribute(ELEMENTS['ELEMENTS_OLPN']['element_get_checked']) == 'true'
                    if not is_checked:
                        try:
                            item.click()
                        except:
                            driver.execute_script('arguments[0].click();', item)
                        logger.info(f'item {nome} selecionado com sucesso', extra={
                            'job': 'data_extraction_olpn',
                            'status': 'success'
                        })
        
        confirmar = wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENTS['ELEMENTS_OLPN']['element_confirm'])
        ))
        if confirmar:
            confirmar.click()
            logger.info('formulario olpn preenchido com sucesso, iniciando download', extra={
                'job': 'data_extraction_olpn',
                'status': 'success'
            })
        
        if wait_download_csv(dir=control_dir):
            logger.info('download do arquivo olpn concluido', extra={
                'job': 'data_extraction_olpn',
                'status': 'success'
            })
        else:
            logger.critical('download do arquivo olpn falhou', extra={
                'job': 'data_extraction_olpn',
                'status': 'failure'
            })

    except Exception as e:
        logger.exception(f'erro ao extrair dados do oLPN: {e}', extra={
            'job': 'data_extraction_olpn',
            'status': 'failure'
        })

    finally:
        driver.quit()

def data_extraction_olpn_from_file(cookies_path: str, download_dir: Path) -> None:
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    data_extraction_olpn(cookies, download_dir)