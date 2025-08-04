# remote imports
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import json

# local imports
from utils.config_logger import setup_logger, log_with_context
from config.settings import TEMP_DIR, LINKS, ELEMENTS, PASSWORD, EMAIL
from utils.reader import clear_dirs
from utils.browser_setup import init_browser

# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='login_csi', logger=logger)
def login_csi(download_dir: Path) -> list[dict] | None:
    """
    log in to the CSI system using Selenium
    """

    driver = None
    cookies = None

    # limpeza de diretorio
    try:
        clear_dirs(TEMP_DIR)
    except Exception as e:
        logger.error(f'erro ao limpar o diretorio temporario: {e}', extra={
            'job': 'login_csi',
            'status': 'failure'
        })
    
    # inicializacao e configuracao da instancia
    try:
        driver = init_browser(download_dir)
        wait = WebDriverWait(driver, 30)
    except Exception as e:
        logger.exception(f'erro ao configurar instancia: {e}', extra={
            'job': 'login_csi',
            'status': 'failure'
        })
        return None
    
    try:
        # acessando login page
        try:
            driver.get(LINKS['LOGIN_CSI'])
            logger.info('navegando para a pagina de login do CSI', extra={
                'job': 'login_csi',
                'status': 'started'
            })
            time.sleep(2)
        except Exception as e:
            logger.critical(f'erro ao acessar a pagina de login do CSI: {e}', extra={
                'job': 'login_csi',
                'status': 'failure'
            })
            return None
        
        # verificacao de elemento (titulo da pagina de login)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, ELEMENTS['ELEMENTS_LOGIN']['element_title'])))
            logger.info('elemento de titulo da pagina de login encontrado', extra={
                'job': 'login_csi',
                'status': 'success'
            })
            time.sleep(2)
        except Exception as e:
            logger.critical(f'elemento de titulo da pagina de login nao encontrado: {e}', extra={
                'job': 'login_csi',
                'status': 'failure'
            })
            return None

        # verificacao de elemento (opcao de login - AZURE AD)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['namespace_dropdown_button']))).click()
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['namespace_azuread']))).click()
            logger.info('namespace Azure AD selecionado', extra={
                'job': 'login_csi',
                'status': 'success'
            })
            time.sleep(2)
        except Exception as e:
            logger.critical(f'erro ao selecionar o namespace Azure AD: {e}', extra={
                'job': 'login_csi',
                'status': 'failure'
            })
            return None
        
        # verificacao de elemento (banner de login)
        try:
            wait.until(EC.presence_of_element_located((By.ID, ELEMENTS['ELEMENTS_LOGIN']['element_banner'])))
            logger.info('banner de login encontrado', extra={
                'job': 'login_csi',
                'status': 'success'
            })
            time.sleep(2)
        except Exception as e:
            logger.critical(f'banner de login nao encontrado: {e}', extra={
                'job': 'login_csi',
                'status': 'failure'
            })
            return None

        # preenchimento de elemento (email)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['email']))).send_keys(EMAIL)
            logger.info('email preenchido', extra={
                'job': 'login_csi',
                'status': 'success'
            })
            time.sleep(2)
        except Exception as e:
            logger.critical(f'erro ao preencher o email: {e}', extra={
                'job': 'login_csi',
                'status': 'failure'
            })
            return None

        # interação com elemento (confirmacao de email)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['submit_button']))).click()
            logger.info('botao de confirmacao de email clicado', extra={
                'job': 'login_csi',
                'status': 'success'
            })
            time.sleep(2)
        except Exception as e:
            logger.critical(f'erro ao clicar no botao de confirmacao de email: {e}', extra={
                'job': 'login_csi',
                'status': 'failure'
            })
            return None

        # preenchimento de elemento (password)
        try:
            wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['password']))).send_keys(PASSWORD)
            logger.info('senha preenchida', extra={
                'job': 'login_csi',
                'status': 'success'
            })
            time.sleep(2)
        except Exception as e:
            logger.critical(f'erro ao preencher a senha: {e}', extra={
                'job': 'login_csi',
                'status': 'failure'
            })
            return None
            
        # interação com elemento (confirmacao de senha e confirmacao de login)
        for i in range(2):
            try:
                wait.until(EC.element_to_be_clickable((By.ID, ELEMENTS['ELEMENTS_LOGIN']['submit_button']))).click()
                logger.info(f'botao de confirmacao de senha clicado ({i+1}/2)', extra={
                    'job': 'login_csi',
                    'status': 'success'
                })
                time.sleep(2)
            except Exception as e:
                logger.critical(f'erro ao clicar no botao de confirmacao de senha ({i+1}/2): {e}', extra={
                    'job': 'login_csi',
                    'status': 'failure'
                })
                return None
        
        # verificação de elemento (titulo da pagina primaria CSI)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, ELEMENTS['ELEMENTS_LOGIN']['element_title_v2'])))
            logger.info('titulo da pagina primaria CSI validado', extra={
                'job': 'login_csi',
                'status': 'success'
            })
            time.sleep(2)
        except Exception as e:
            logger.critical(f'titulo da pagina primaria CSI nao encontrado: {e}', extra={
                'job': 'login_csi',
                'status': 'failure'
            })
            return None
        
        logger.info('login no CSI realizado com sucesso', extra={
            'job': 'login_csi',
            'status': 'success'
        })

        cookies = driver.get_cookies()

        with open("cookies.json", 'w', encoding='utf-8') as f:
            json.dump(cookies, f)

    except Exception as e:
        logger.critical(f'erro durante o login: {e}', extra={
            'job': 'login_csi',
            'status': 'failure'
        })
        return None
    
    finally:
        if driver:
            driver.quit()
    
    return cookies