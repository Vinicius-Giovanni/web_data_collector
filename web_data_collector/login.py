# remote imports
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# local imports
from utils.config_logger import setup_logger, log_with_context
from config.settings import TEMP_DIR, LINKS, ELEMENTS
from utils.reader import clear_dirs
from utils.browser_setup import init_browser

# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='login_csi')
def login_csi():
    """
    log in to the CSI system using Selenium
    """

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
        driver = init_browser()
        wait = WebDriverWait(driver, 30)
    except Exception as e:
        logger.exception(f'erro ao configurar instancia: {e}', extra={
            'job': 'login_csi',
            'status': 'failure'
        })
        return
    
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
            return
        
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

        


    except Exception as e:
        logger.critical(f'erro durante o login: {e}', extra={
            'job': 'login_csi',
            'status': 'failure'
        })