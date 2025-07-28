# remote imports
from selenium import webdriver
from config.settings import TEMP_DIR
from selenium.webdriver.chrome.options import Options
import os

# local imports
from utils.config_logger import setup_logging, log_with_context

# %(name)s <<< module name
logger = setup_logging(__name__)

try:
    logger.info('verificacao do diretorio temporario', extra={
        'job': 'browser_setup',
        'status': 'started'
    })
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    logger.info('diretorio temporario verificado', extra={
        'job': 'browser_setup',
        'status': 'success'
    })
except Exception as e:
    logger.warning(f'erro ao verificar o diretorio temporario: {e}', extra={
        'job': 'browser_setup',
        'status': 'failure'
    })

@log_with_context(job='get_chrome_options')
def get_chrome_options() -> Options:
    """
    configure of options for the chrome browser
    """

    logger.info('iniciando configuracao do Chrome', extra={
        'job': 'get_chrome_options',
        'status': 'started'
    })

    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)

    if os.getenv('CHROME_HEADLESS', 'false').lower() == 'true':
        options.add_argument('--headless=new')

    prefs = {
        'download.default_directory': str(TEMP_DIR),
        'download.prompt_for_download': False,
        'directory_upgrade': True,
        'safebrowsing.enabled': True,
        'profile.default_content_setting_values.automatic_downloads':1,
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False
    }
    options.add_experimental_option('prefs', prefs)

    logger.info('Chrome configurado.')

    logger.info('configuracao do Chrome concluida', extra={
        'job': 'get_chrome_options',
        'status': 'success'
    })

    return options

def init_browser() -> webdriver.Chrome:
    options = get_chrome_options()
    driver = webdriver.Chrome(options=options)
    return driver