from utils.config_logger import setup_logger
from web_data_collector.login import login_csi
from config.settings import TEMP_DIR, FILE_ROUTER
from web_data_collector.olpn import data_extraction_olpn
from utils.reader import forward_files_by_name
from pipelines.standard_pipeline.olpn_pipeline import OlpnPipeline

import time

logger = setup_logger(__name__)

pipeline_olpn = OlpnPipeline()

def main():
    driver = login_csi()
    data_extraction_olpn(driver)
    time.sleep(2)
    forward_files_by_name(input_folder=TEMP_DIR['BRONZE'], file_router=FILE_ROUTER)
    driver.quit()
    time.sleep(2)
    pipeline_olpn.run(input_path=TEMP_DIR['SILVER']['olpn'], output_path=TEMP_DIR['GOLD']['olpn'])

if __name__ == "__main__":
    main()