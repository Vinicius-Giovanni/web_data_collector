from utils.config_logger import setup_logger
from web_data_collector.login import login_csi
from config.settings import TEMP_DIR
from web_data_collector.olpn import data_extraction_olpn
from utils.reader import function_distribution

import time

logger = setup_logger(__name__)

def main():
    logger.info('iniciando automacao web_data_collector', extra={
        'job': 'main',
        'status': 'started'
    })
    driver = login_csi()
    data_extraction_olpn(driver)
    time.sleep(2)
    function_distribution(TEMP_DIR['DIR_CHROME'])
    driver.quit()
    logger.info('finalizando automacao web_data_collector', extra={
        'job': 'main',
        'status': 'finished'
    })
    # print(TEMP_DIR['DIR_CHROME'])



if __name__ == "__main__":
    main()