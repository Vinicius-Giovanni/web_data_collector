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

# remote imports
import sys
import multiprocessing

logger = setup_logger(__name__)

pipeline_olpn = OlpnPipeline()
pipeline_picking = PickingPipeline()

@log_with_context(job='run_with_pipeline', logger=logger)
def run_with_pipeline(extract_func, extract_args, pipeline_func, input_path, output_path):
    try:
        # extraction
        extract_func(*extract_args)
        logger.info(f'extracao finalizada: {extract_func.__name__}')

        # call pipeline to ending extraction
        pipeline_func(input_path=input_path, output_path=output_path)
        logger.info(f'pipeline finalizado: {pipeline_func.__name__}')
    except Exception as e:
        logger.error(f'erro ao executar {extract_func.__name__} ou {pipeline_func.__name__}', exc_info=True)
        sys.exit(1)

@log_with_context(job='main', logger=logger)
def main():
    cookies = login_csi(TEMP_DIR['BRONZE']['dir_chrome_login'])

    if not cookies:
        logger.error('login falhou: cookies nao obtidos. abortando processo')
        sys.exit(1)

    t1 = multiprocessing.Process(target=run_with_pipeline, args=(
        data_extraction_olpn_from_file,
        ("cookies.json", TEMP_DIR['BRONZE']['olpn']),
        pipeline_olpn,
        TEMP_DIR['BRONZE']['olpn'], 
        TEMP_DIR['SILVER']['olpn']
        )
    )

    t2 = multiprocessing.Process(target=run_with_pipeline, args=(
        data_extraction_cancel_from_file,
        ("cookies.json", TEMP_DIR['BRONZE']['cancel']),
        pipeline_picking,
        TEMP_DIR['BRONZE']['cancel'],
        TEMP_DIR['SILVER']['cancel']
        )
    )

    t3 = multiprocessing.Process(target=data_extraction_picking_from_file, args=("cookies.json", TEMP_DIR['BRONZE']['picking']))
    t4 = multiprocessing.Process(target=data_extraction_putaway_from_file, args=("cookies.json", TEMP_DIR['BRONZE']['putaway']))
    t5 = multiprocessing.Process(target=data_extraction_packing_from_file, args=("cookies.json", TEMP_DIR['BRONZE']['packing']))
    t6 = multiprocessing.Process(target=data_extraction_loading_from_File, args=("cookies.json", TEMP_DIR['BRONZE']['loading']))

    for t in [t1, t2]:
        t.start()

    for t in [t1, t2]:
        t.join()

if __name__ == "__main__":
    main()