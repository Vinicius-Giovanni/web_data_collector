import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json
import locale
from utils.config_logger import setup_logger, log_with_context
from config.settings import LINKS, ELEMENTS, PASSWORD, EMAIL, DATA_PATHS, CLEAR_DIR
from utils.reader import clear_dirs
from utils.browser_setup import init_browser
from utils.get_info import load_penultimate_dates, get_yesterday_date

logger = setup_logger(__name__)

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

chamada_funcao_dates = load_penultimate_dates(DATA_PATHS['gold'], date_format= '%d/%m/%Y')
yesterday_date = get_yesterday_date()
yesterday_date_format =  get_yesterday_date(format='%b %Y')
chamada_funcao_dates_format = load_penultimate_dates(DATA_PATHS['gold'], date_format= '%b %Y')

penultimate_date_cancel = chamada_funcao_dates['cancel'] or yesterday_date

penultimate_date_loading_format = chamada_funcao_dates_format['loading'] or yesterday_date_format
penultimate_date_loading = chamada_funcao_dates['loading'] or yesterday_date

penultimate_date_olpn = chamada_funcao_dates['olpn'] or yesterday_date

penultimate_date_packing_format = chamada_funcao_dates_format['packing'] or yesterday_date_format
penultimate_date_packing = chamada_funcao_dates['packing'] or yesterday_date

penultimate_date_picking = chamada_funcao_dates['picking'] or yesterday_date

penultimate_date_putaway = chamada_funcao_dates['putaway'] or yesterday_date

@log_with_context(job='login_csi', logger=logger)
def login_csi(download_dir: Path) -> list[dict] | None:

    driver = None
    cookies = None

    try:
        clear_dirs(CLEAR_DIR)
    except Exception as e:
        logger.error(f'nao foi possivel limpar os diretorios temporarios', extra={'status': 'falha'})
    
    try:
        driver = init_browser(download_dir)
        wait = WebDriverWait(driver, 30)
    except Exception as e:
        logger.exception(f'instancia aberta', extra={'status': 'sucesso'})
        return None
    
    try:
        try:
            driver.get(LINKS['LOGIN_CSI'])
            time.sleep(2)
        except Exception as e:
            logger.critical(f'instancia nao acessada', extra={'status': 'critico'})
            return None
        
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, ELEMENTS['ELEMENTS_LOGIN']['element_title'])))
            time.sleep(2)
        except Exception as e:
            return None

        try:
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['namespace_dropdown_button']))).click()
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['namespace_azuread']))).click()
            time.sleep(2)
        except Exception as e:
            return None
        
        try:
            wait.until(EC.presence_of_element_located((By.ID, ELEMENTS['ELEMENTS_LOGIN']['element_banner'])))
            time.sleep(2)
        except Exception as e:
            return None

        try:
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['email']))).send_keys(EMAIL)
            time.sleep(2)
        except Exception as e:
            return None

        try:
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['submit_button']))).click()
            time.sleep(2)
        except Exception as e:
            return None

        try:
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['password']))).send_keys(PASSWORD)
            time.sleep(2)
        except Exception as e:
            return None
            
        for i in range(2):
            try:
                wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['submit_button']))).click()
                time.sleep(2)
            except Exception as e:
                return None

        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, ELEMENTS['ELEMENTS_LOGIN']['element_title_v2'])))
            time.sleep(2)
        except Exception as e:
            return None
        
        logger.info('iniciando extracao de cookies', extra={'status': 'iniciado'})

        cookies = driver.get_cookies()

        with open("cookies.json", 'w', encoding='utf-8') as f:
            json.dump(cookies, f)

    except Exception as e:
        logger.critical(f'download do relatorio 5.04 - Produtividade Load - Load falhou', extra={'status': 'critico'})
        return None
    
    finally:
        if driver:
            driver.quit()
    
    return cookies