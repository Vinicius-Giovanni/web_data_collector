from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
from utils.config_logger import log_with_context
from config.pipeline_config import logger
from config.paths import TEMP_DIR
from config.elements import ELEMENTS
from config.pipeline_config import LINKS
from utils.reader import wait_download_csv
from utils.browser_setup import create_authenticated_driver
from web_data_collector.login import yesterday_date, penultimate_date_cancel

star_date = None
end_date = None
control_dir = TEMP_DIR['BRONZE']['cancel'] # <<< folder monitored by the "wait_download_csv" function

@log_with_context(job='data_extraction_cancel', logger=logger)
def data_extraction_cancel(cookies: list[dict], dowload_dir: Path) -> None:
    driver = create_authenticated_driver(cookies, download_dir=dowload_dir)

    try:
        wait = WebDriverWait(driver, 30)
        driver.get(LINKS['LOGIN_CANCEL'])

        logger.info('instancia aberta', extra={'status': 'sucesso'})

        # verificando se o frame esta disponivel e acessando
        if not wait.until(EC.frame_to_be_available_and_switch_to_it(
            (By.XPATH, ELEMENTS['frame']))):
            logger.critical('iframe nao encontrado', extra={'status': 'critico'})

        logger.info('iniciando extracao do relatorio 6.10 - Pedidos Cancelados', extra={'status': 'iniciado'})

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

        if wait_download_csv(dir=control_dir):
            logger.info('download do relatorio 6.10 - Pedidos Cancelados concluido', extra={'status': 'sucesso'})
        else:
            logger.warning('download do relatorio 6.10 - Pedidos Cancelados nao encontrado no diretorio configurado', extra={'status': 'perigoso'})

    except Exception as e:
        logger.critical(f'nao foi possivel extrair o relatorio 6.10 - Pedidos Cancelados', extra={'status': 'critico'})

    finally:
            driver.quit()

def data_extraction_cancel_from_file(cookies_path: str, download_dir: Path) -> None:
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    data_extraction_cancel(cookies, download_dir)