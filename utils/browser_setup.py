from selenium import webdriver
from config.paths import TEMP_DIR, SELENIUM_CHROME
from config.pipeline_config import LINKS
from selenium.webdriver.chrome.options import Options
import os
from pathlib import Path
import time 
import json
import tempfile
import uuid
from utils.config_logger import log_with_context
from config.pipeline_config import logger
try:
    logger.info('verificacao do diretorio temporario', extra={
        'job': 'browser_setup',
        'status': 'started'
    })

    for layer, dataset in TEMP_DIR.items(): # layer = BRONZE, SILVER, GOLD
        for dataset, path in dataset.items():
            if not path.exists:
                logger.warning(f'diretorio temporario {layer}/{dataset} nao existe, criando...', extra={
                    'job': 'browser_setup',
                    'status': 'warning'
                })
                path.mkdir(parents=True, exist_ok=True)
    
    logger.info('diretorio temporario verificado com sucesso', extra={
        'job': 'browser_setup',
        'status': 'warning'
    })

except Exception as e:
    logger.warning(f'erro ao verificar o diretorio temporario', extra={
        'job': 'browser_setup',
        'status': 'failure'
    })

@log_with_context(job='get_chrome_options', logger=logger)
def get_chrome_options(path_temp_dir: str | Path) -> Options:
    """
    configure of options for the chrome browser
    """

    logger.info('iniciando configuracao do chrome', extra={
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

    user_data_dir = tempfile.mkdtemp(prefix=f'chrome_profile_{uuid.uuid4()}')
    

    if os.getenv('CHROME_HEADLESS', 'false').lower() == 'true':
        options.add_argument(f'--headless=new')
    
    options.add_argument(f'--user-data-dir={user_data_dir}')

    prefs = {
        'download.default_directory': str(path_temp_dir),
        'download.prompt_for_download': False,
        'directory_upgrade': True,
        'safebrowsing.enabled': True,
        'profile.default_content_setting_values.automatic_downloads':1,
        'credentials_enable_service': False,
        'profile.password_manager_enabled': False
    }
    options.add_experimental_option('prefs', prefs)

    logger.info('chrome configurado')

    logger.info('configuracao do Chrome concluida', extra={
        'job': 'get_chrome_options',
        'status': 'success'
    })

    return options

def init_browser(download_dir: str) -> webdriver.Chrome:
    options = get_chrome_options(download_dir)
    driver = webdriver.Chrome(options=options)
    return driver

@log_with_context(job='create_authenticated_driver', logger=logger)
def create_authenticated_driver(cookies: list[dict], download_dir: Path) -> webdriver:

    driver = init_browser(download_dir=download_dir)

    time.sleep(1)

    driver.get(LINKS['LOGIN_CSI'])

    for cookie in cookies:
        try:
            if 'samaSite' in cookie:
                cookie.pop('sameSite') # evita erro em chromes headless
            driver.add_cookie(cookie)
        
        except Exception as e:
            logger.warning(f'cookie invalido descartado {cookie} motivo {e}', extra={
                'job': 'create_authenticated_driver',
                'status': 'failure'
            })
        

    driver.get(LINKS['LOGIN_CSI']) # reload instance

    return driver

def load_cookies(path='cookies.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)