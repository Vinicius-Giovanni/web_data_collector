from utils.config_logger import setup_logger
from web_data_collector.login import login_csi
from config.settings import PASSWORD, EMAIL
from web_data_collector.olpn import data_extraction_olpn

import time

logger = setup_logger(__name__)

def main():
    logger.info('iniciando automacao web_data_collector', extra={
        'job': 'main',
        'status': 'started'
    })
    driver = login_csi()
    data_extraction_olpn(driver)
    time.sleep(5) 
    driver.quit()
    logger.info('finalizando automacao web_data_collector', extra={
        'job': 'main',
        'status': 'finished'
    })



if __name__ == "__main__":
    main()