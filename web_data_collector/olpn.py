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
from web_data_collector.login import penultimate_date_olpn, yesterday_date

star_date = yesterday_date # <<< penultimate update date in the gold/olpn folder
end_date = yesterday_date # <<< current date entered in the final data field
control_dir = TEMP_DIR['BRONZE']['olpn'] # <<< folder monitored by the "wait_download_csv" function

@log_with_context(job='data_extraction_olpn', logger=logger)
def data_extraction_olpn(cookies: list[dict], dowload_dir: Path) -> None:

    driver = create_authenticated_driver(cookies, download_dir=dowload_dir)

    try:

        for filial_value in ELEMENTS['ELEMENTS_OLPN']['element_filial']:
            wait = WebDriverWait(driver, 30)
            driver.get(LINKS['LOGIN_OLPN'])

            logger.info('instancia aberta', extra={'status': 'sucesso'})

            if not wait.until(EC.frame_to_be_available_and_switch_to_it(
                (By.XPATH, ELEMENTS['frame']))):
                logger.error('iframe nao encontrado', extra={'status': 'critico'})

            logger.info('iniciando extracao do relatorio 3.11 - Status Wave + oLPN', extra={'status': 'iniciado'})
            

            filial = wait.until(EC.element_to_be_clickable(
                (By.ID, ELEMENTS['ELEMENTS_OLPN']['element_filial_id']))
            )
            if filial:
                Select(filial).select_by_value(filial_value)

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
                            logger.info(f'item {nome} selecionado', extra={'status': 'sucesso'})
            
            confirmar = wait.until(EC.element_to_be_clickable(
                (By.ID, ELEMENTS['ELEMENTS_OLPN']['element_confirm'])
            ))
            if confirmar:
                confirmar.click()
                logger.critical('erro na selecao de tipo de pedidos', extra={'status': 'critico'})
            
            if wait_download_csv(dir=control_dir):
                logger.info('download do relatorio 3.11 - Status Wave + oLPN concluido', extra={'status': 'sucesso'})
            else:
                logger.critical('download do relatorio 3.11 - Status Wave + oLPN concluido falhou', extra={'status': 'critico'})

    except Exception as e:
        logger.exception(f'download do relatorio 3.11 - Status Wave + oLPN concluido falhou', extra={'status': 'critico'})

    finally:
        driver.quit()

def data_extraction_olpn_from_file(cookies_path: str, download_dir: Path) -> None:
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    data_extraction_olpn(cookies, download_dir)