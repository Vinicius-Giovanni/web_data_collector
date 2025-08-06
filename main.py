# local imports
from utils.config_logger import setup_logger, log_with_context
from web_data_collector.login import login_csi
from config.settings import TEMP_DIR, FILE_ROUTER, DATA_PATHS
from web_data_collector.olpn import data_extraction_olpn_from_file
from web_data_collector.cancel import data_extraction_cancel_from_file
from web_data_collector.picking import data_extraction_picking_from_file
from web_data_collector.putaway import data_extraction_putaway_from_file
from pipelines.standard_pipeline.olpn_pipeline import OlpnPipeline

# remote imports
import sys
import multiprocessing

logger = setup_logger(__name__)

pipeline_olpn = OlpnPipeline()

@log_with_context(job='main', logger=logger)
def main():
    cookies = login_csi(TEMP_DIR['BRONZE']['dir_chrome_login'])

    if not cookies:
        logger.error('login falhou: cookies nao obtidos. abortando processo')
        sys.exit(1)

    t1 = multiprocessing.Process(target=data_extraction_olpn_from_file, args=("cookies.json", TEMP_DIR['BRONZE']['olpn']))
    t2 = multiprocessing.Process(target=data_extraction_cancel_from_file, args=("cookies.json", TEMP_DIR['BRONZE']['cancel']))
    t3 = multiprocessing.Process(target=data_extraction_picking_from_file, args=("cookies.json", TEMP_DIR['BRONZE']['picking']))
    t4 = multiprocessing.Process(target=data_extraction_putaway_from_file, args=("cookies.json", TEMP_DIR['BRONZE']['putaway']))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    # Após as extrações finalizadas, deve ser ativado os pipelines. Por exemplo,a t1 finalizou, então já pode ativar o pipeline referente a ela

    # pipeline_olpn.run(input_path=TEMP_DIR['BRONZE']['olpn'], output_path=TEMP_DIR['SILVER']['olpn'])


if __name__ == "__main__":
    main()