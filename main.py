# local imports
from utils.config_logger import setup_logger, log_with_context
from web_data_collector.login import login_csi
from config.settings import TEMP_DIR, FILE_ROUTER, DATA_PATHS
from web_data_collector.olpn import data_extraction_olpn_from_file
from web_data_collector.cancel import data_extraction_cancel_from_file
from web_data_collector.picking import data_extraction_picking_from_file
from web_data_collector.putaway import data_extraction_putaway_from_file
from web_data_collector.packing import data_extraction_packing_from_file
from web_data_collector.loading import data_extraction_loading_from_File
from pipelines.standard_pipeline.olpn_pipeline import OlpnPipeline
from pipelines.standard_pipeline.picking_pipeline import PickingPipeline
from pipelines.standard_pipeline.cancel_pipeline import CancelPipeline
from pipelines.standard_pipeline.putaway_pipeline import PutawayPipeline

# remote imports
import sys
import multiprocessing

logger = setup_logger(__name__)

def run_pipeline(pipeline_class, input_path, output_path):
    """
    runs the pipeline with the given class, input path, and output path
    """
    pipeline = pipeline_class()
    pipeline.run(input_path=input_path, output_path=output_path)
    logger.info(f'pipeline {pipeline_class.__name__} finalizado')

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
    t5 = multiprocessing.Process(target=data_extraction_packing_from_file, args=("cookies.json", TEMP_DIR['BRONZE']['packing']))
    t6 = multiprocessing.Process(target=data_extraction_loading_from_File, args=("cookies.json", TEMP_DIR['BRONZE']['loading']))

    for t in [t1,t2,t3, t4]:
        t.start()

    for t in [t1,t2,t3,t4]:
        t.join()

    logger.info('processos de extracao finalizados')

    p1 = multiprocessing.Process(
        target=run_pipeline,
        args=(OlpnPipeline,
                TEMP_DIR['BRONZE']['olpn'],
                TEMP_DIR['SILVER']['olpn']))
    
    p2 = multiprocessing.Process(
        target=run_pipeline,
        args=(PickingPipeline,
              TEMP_DIR['BRONZE']['picking'],
              TEMP_DIR['SILVER']['picking']))
    
    p3 = multiprocessing.Process(
        target=run_pipeline,
        args=(CancelPipeline,
              TEMP_DIR['BRONZE']['cancel'],
              TEMP_DIR['SILVER']['cancel']))
    
    p4 = multiprocessing.Process(
        target=run_pipeline,
        args=(PutawayPipeline,
              TEMP_DIR['BRONZE']['putaway'],
              TEMP_DIR['SILVER']['putaway']))

    for p in [p1, p2, p3, p4]:
        p.start()
    
    for p in [p1, p2, p3, p4]:
        p.join()
    
    logger.info('pipelines finalizados')

if __name__ == "__main__":
    main()