# local imports
from utils.config_logger import setup_logger, log_with_context
from web_data_collector.login import login_csi
from config.settings import TEMP_DIR, FILE_ROUTER, DATA_PATHS
from web_data_collector.olpn import data_extraction_olpn
from web_data_collector.cancel import data_extraction_cancel
from web_data_collector.picking import data_extraction_picking
from pipelines.standard_pipeline.olpn_pipeline import OlpnPipeline

# remote imports
import time
import sys
import threading

logger = setup_logger(__name__)

pipeline_olpn = OlpnPipeline()

@log_with_context(job='main', logger=logger)
def main():
    cookies = login_csi(TEMP_DIR['BRONZE']['dir_chrome_login'])

    if not cookies:
        logger.error('login falhou: cookies nao obtidos. abortando processo')
        sys.exit(1)

    t1 = threading.Thread(target=data_extraction_olpn, args=(cookies, TEMP_DIR['BRONZE']['olpn']))
    t2 = threading.Thread(target=data_extraction_cancel, args=(cookies, TEMP_DIR['BRONZE']['cancel']))
    t3 = threading.Thread(target=data_extraction_picking, args=(cookies, TEMP_DIR['BRONZE']['picking']))

    # t1.start()
    # t2.start()
    t3.start()

    # t1.join()
    # t2.join()
    t3.join()

    # data_extraction_olpn(cookies, TEMP_DIR['BRONZE']['olpn'])

    # pipeline_olpn.run(input_path=TEMP_DIR['BRONZE']['olpn'], output_path=TEMP_DIR['SILVER']['olpn'])


if __name__ == "__main__":
    main()