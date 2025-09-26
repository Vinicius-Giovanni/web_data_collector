from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
import locale
from datetime import datetime
from utils.config_logger import log_with_context
from config.pipeline_config import logger, LINKS
from config.paths import TEMP_DIR
from config.elements import ELEMENTS
from utils.reader import wait_download_csv
from utils.browser_setup import create_authenticated_driver
from web_data_collector.login import penultimate_date_packing_format, penultimate_date_packing, yesterday_date_format, yesterday_date

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

star_date = penultimate_date_packing_format # <<< penultimate update date in the gold/olpn folder
day_star_date = datetime.strptime(penultimate_date_packing, "%d/%m/%Y").day
id_star_date = f'{ELEMENTS['ELEMENTS_PACKING']['id_dia_inicio']}{day_star_date}'
end_date = yesterday_date_format # <<< current date entered in the final data field
day_end_date = datetime.strptime(yesterday_date, "%d/%m/%Y").day
id_end_date = f'{ELEMENTS['ELEMENTS_PACKING']['id_dia_fim']}{day_end_date}'
control_dir = TEMP_DIR['BRONZE']['packing'] # <<< folder monitored by the "wait_download_csv" function

@log_with_context(job='data_extraction_packing', logger=logger)
def data_extraction_packing(cookies: list[dict], dowload_dir: Path) -> None:

    driver = create_authenticated_driver(cookies, download_dir=dowload_dir)

    try:
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
            Select(filial).select_by_value(ELEMENTS['ELEMENTS_PACKING']['element_filial'])

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

        while dt_start_string != star_date:
            logger.info(f'{dt_start_string} != {star_date}, retornando...', extra={'status': 'iniciado'})
            wait.until(EC.element_to_be_clickable(
                (By.ID, ELEMENTS['ELEMENTS_PACKING']['calendario_start']['retornar'])
            )).click()
        
        logger.info(f'{dt_start_string} = {star_date}, selecionando...',extra={'status': 'sucesso'})
        wait.until(EC.element_to_be_clickable(
            (By.ID, id_end_date)
        )).click()
        logger.info(f'data inicio preenchida: data: {dt_start_string} id: {id_end_date}', extra={'status': 'sucesso'})

        while dt_end_string != end_date:
            logger.info(f'{dt_end_string} != {end_date}, retornando...', extra={'status': 'iniciado'})
            wait.until(EC.element_to_be_clickable(
                (By.ID, ELEMENTS['ELEMENTS_PACKING']['calendario_end']['retornar'])
            )).click()

        logger.info(f'{dt_end_string} = {end_date}, selecionando...',extra={'status': 'sucesso'})

        wait.until(EC.element_to_be_clickable(
            (By.ID, id_star_date)
        )).click()

        logger.info(f'{dt_end_string} = {end_date}, selecionando...',extra={'status': 'sucesso'})

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
                        
        confirmar = wait.until(EC.element_to_be_clickable(
            (By.ID, ELEMENTS['ELEMENTS_PACKING']['element_confirm'])
        ))
        if confirmar:
            confirmar.click()
        else:
            logger.critical('erro na selecao de tipo de pedidos', extra={'status': 'critico'})
        
        if wait_download_csv(dir=control_dir):
            logger.info('download do relatorio 5.03 - Produtividade de Packing - Packed por hora concluido', extra={'status': 'sucesso'})
        else:
            logger.critical('download do relatorio 5.03 - Produtividade de Packing - Packed por hora falhou', extra={'status': 'critico'})

    except Exception as e:
        logger.critical('download do relatorio 5.03 - Produtividade de Packing - Packed por hora falhou', extra={'status': 'critico'})
    finally:
        driver.quit()


def data_extraction_packing_from_file(cookies_path: str, download_dir: Path) -> None:
    with open(cookies_path, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    data_extraction_packing(cookies, download_dir)