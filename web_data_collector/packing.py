from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
from utils.config_logger import log_with_context
import locale
from datetime import datetime
from utils.config_logger import log_with_context
from config.pipeline_config import logger, LINKS
from config.paths import TEMP_DIR
from config.elements import ELEMENTS
from utils.reader import wait_download_csv
from utils.browser_setup import create_authenticated_driver
import inspect
from collections.abc import Callable
import time

@log_with_context(job='data_extraction_packing', logger=logger)
def data_extraction_packing(cookies: list[dict],
                         download_dir: Path,
                         parquet_folder: Path | None,
                         entry_date: str | Callable,
                         exit_date: str | Callable,
                         id_data_entry = str,
                         id_exit_data = str) -> None:
    
    if callable(entry_date):
        sig = inspect.signature(entry_date)
        if 'parquet_folder' in sig.parameters:
            entry_date = entry_date(parquet_folder)
        else:
            entry_date = entry_date()
    
    if callable(exit_date):
        sig = inspect.signature(exit_date)
        if 'parquet_folder' in sig.parameters:
            exit_date = exit_date(parquet_folder)
        else:
            exit_date = exit_date()

    id_data_entry = int(entry_date.split('/')[0])
    id_start_date = f'{ELEMENTS['ELEMENTS_LOADING']['id_dia_fim']}{id_data_entry}'

    id_exit_data = int(exit_date.split('/')[0])
    id_end_date = f'{ELEMENTS['ELEMENTS_PACKING']['id_dia_fim']}{id_exit_data}'

    driver = create_authenticated_driver(cookies, download_dir=download_dir)

    try:

        for filial_value in ELEMENTS['ELEMENTS_PACKING']['element_filial']:
            wait = WebDriverWait(driver, 30)
            driver.get(LINKS['LOGIN_PACKING'])

            logger.info('instancia aberta', extra={'status': 'sucesso'})

            if not wait.until(EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, ELEMENTS['frame']))):
                logger.critical('iframe nao encontrado', extra={'status': 'critico'})

            logger.info('iniciando extracao do relatorio 5.03 - Produtividade de Packing - Packed por hora', extra={'status': 'iniciado'})

            filial = wait.until(EC.element_to_be_clickable(
                (By.ID, ELEMENTS['ELEMENTS_PACKING']['element_filial_id'])
            ))
            if filial:
                Select(filial).select_by_value(filial_value)

            if wait.until(EC.visibility_of_element_located(
                (By.XPATH, ELEMENTS['ELEMENTS_PACKING']['element_listbox']))):

                itens = driver.find_elements(By.XPATH, ELEMENTS['ELEMENTS_PACKING']['elements_listbox'])

                for item in itens:
                    nome = item.get_attribute(ELEMENTS['ELEMENTS_PACKING']['element_get_item'])
                    if nome in ELEMENTS['ELEMENTS_PACKING']['list_itens']:
                        is_checked = item.get_attribute(ELEMENTS['ELEMENTS_PACKING']['element_get_checked']) == 'true'
                        if not is_checked:
                            try:
                                item.click()
                            except:
                                driver.execute_script('arguments[0].click();', item)
                            logger.info(f'item {nome} selecionado com sucesso', extra={'status': 'sucesso'})

            dt_start = wait.until(EC.presence_of_element_located(
                (By.XPATH, ELEMENTS['ELEMENTS_PACKING']['element_dt_start'])
            ))

            dt_end = wait.until(EC.presence_of_element_located(
                (By.XPATH, ELEMENTS['ELEMENTS_PACKING']['element_dt_end'])
            ))

            if dt_start:
                dt_start_string = dt_start.get_attribute("value")

            if dt_end:
                dt_end_string = dt_end.get_attribute("value")

            while dt_start_string != entry_date:

                logger.info(f'{dt_start_string} != {entry_date}, retornando...', extra={'status': 'iniciado'})
                time.sleep(2)
                wait.until(EC.element_to_be_clickable(
                    (By.ID, ELEMENTS['ELEMENTS_LOADING']['calendario_start']['retornar'])
                )).click()
                
                logger.info(f'{dt_start_string} = {entry_date}, selecionando...', extra={'status': 'sucesso'})
                time.sleep(2)
                wait.until(EC.element_to_be_clickable(
                    (By.ID, id_start_date)
                )).click()

                dt_start_string = dt_start.get_attribute('value')

            logger.info(f'data inicio preenchida: data: {dt_start_string} id: {id_end_date}', extra={'status': 'sucesso'})

            while dt_end_string != exit_date:

                logger.info(f'{dt_end_string} != {exit_date}, retornando...', extra={'status': 'iniciado'})
                time.sleep(2)
                wait.until(EC.element_to_be_clickable(
                    (By.ID, ELEMENTS['ELEMENTS_LOADING']['calendario_end']['retornar'])
                )).click()
            
                logger.info(f'{dt_end_string} = {exit_date}, selecionando...', extra={'status': 'sucesso'})
                time.sleep(2)
                wait.until(EC.element_to_be_clickable(
                    (By.ID, id_end_date)
                )).click()

                dt_end_string = dt_end.get_attribute("value")

            logger.info(f'{dt_end_string} = {exit_date}, selecionando...',extra={'status': 'sucesso'})
                            
            confirmar = wait.until(EC.element_to_be_clickable(
                (By.ID, ELEMENTS['ELEMENTS_PACKING']['element_confirm'])
            ))
            if confirmar:
                confirmar.click()
            else:
                logger.critical('erro na selecao de tipo de pedidos', extra={'status': 'critico'})
            
            if wait_download_csv(dir=TEMP_DIR['BRONZE']['packing']):
                logger.info('download do relatorio 5.03 - Produtividade de Packing - Packed por hora concluido', extra={'status': 'sucesso'})
            else:
                logger.critical('download do relatorio 5.03 - Produtividade de Packing - Packed por hora falhou', extra={'status': 'critico'})

    except Exception as e:
        logger.critical('download do relatorio 5.03 - Produtividade de Packing - Packed por hora falhou', extra={'status': 'critico'})
    finally:
        driver.quit()


def data_extraction_packing_from_file(cookies_path: str,
                         download_dir: Path,
                         parquet_folder: Path | None,
                         entry_date: str | Callable,
                         exit_date: str | Callable,
                         id_data_entry = str,
                         id_exit_data = str) -> None:
    
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
        
    data_extraction_packing(cookies,
                            download_dir,
                            parquet_folder,
                            entry_date, exit_date,
                            id_data_entry,
                            id_exit_data)