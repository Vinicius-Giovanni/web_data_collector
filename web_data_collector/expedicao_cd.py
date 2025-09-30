from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
from utils.config_logger import log_with_context
from config.pipeline_config import logger, LINKS
from config.paths import TEMP_DIR
from config.elements import ELEMENTS
from utils.reader import wait_download_csv
from utils.browser_setup import create_authenticated_driver
import inspect
from collections.abc import Callable

@log_with_context(job='data_extraction_expedicao', logger=logger)
def data_extraction_expedicao(cookies: list[dict],
                              download_dir: Path,
                              parquet_folder: Path,
                              entry_date: str | Callable,
                              exit_date: str | Callable) -> None:
    
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

    driver = create_authenticated_driver(cookies, download_dir=download_dir)

    try:

        for filial_value in ELEMENTS['ELEMENTS_EXPEDICAO']['element_filial']:

                wait = WebDriverWait(driver, 30)
                driver.get(LINKS['LOGIN_EXPEDICAO'])

                logger.info(f'extraindo relatorio 6.06- Expedicao CD da filial: {filial_value}', extra={'status': 'iniciado'})
                logger.info('instancia aberta', extra={'status': 'sucesso'})

                if not wait.until(EC.frame_to_be_available_and_switch_to_it(
                    (By.XPATH, ELEMENTS['frame'])
                )):
                    logger.critical('iframe nao encontrado', extra={'status': 'critico'})

                logger.info('iniciando extracao do relatorio 3.11 - Status Wave + oLPN', extra={'status': 'iniciando'})

                filial = wait.until(EC.element_to_be_clickable(
                    (By.ID, ELEMENTS['ELEMENTS_EXPEDICAO']['element_filial_id'])
                ))
                if filial:
                    Select(filial).select_by_value(filial_value)

                dt_start = wait.until(EC.element_to_be_clickable(
                    (By.ID, ELEMENTS['ELEMENTS_EXPEDICAO']['element_dt_start'])
                ))
                if dt_start:
                    dt_start.clear()
                    dt_start.send_keys(entry_date)
                
                dt_end = wait.until(EC.element_to_be_clickable(
                    (By.ID, ELEMENTS['ELEMENTS_EXPEDICAO']['element_dt_end'])
                ))
                if dt_end:
                    dt_end.clear()
                    dt_end.send_keys(exit_date)
                
                confirmar = wait.until(EC.element_to_be_clickable(
                    (By.ID, ELEMENTS['ELEMENTS_EXPEDICAO']['element_confirm'])
                ))
                if confirmar:
                    confirmar.click()

                if wait_download_csv(dir=TEMP_DIR['BRONZE']['expedicao']):
                    logger.info('download do relatorio 6.06 - Expedicao CD concluido', extra={'status': 'sucesso'})
                else:
                    logger.critical('download do relatorio 6.06 - Expedicao CD falhou', extra={'status': 'critico'})

    except Exception as e:
        logger.critical('download do relatorio 6.06 - Expedicao CD falhou', extra={'status': 'critico'})

    finally:
        driver.quit()

def data_extraction_expedicao_from_file(cookies_path: str,
                                        download_dir: Path,
                                        parquet_folder: Path | None,
                                        entry_date: str | Callable,
                                        exit_date: str | Callable) -> None:
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
        data_extraction_expedicao(cookies, download_dir, parquet_folder, entry_date, exit_date)
