# local imports
from utils.config_logger import setup_logger, log_with_context
from utils.reader import rename_csv_with_yesterday, move_files, merge_parquet, clear_dirs
from web_data_collector.login import login_csi
from config.settings import TEMP_DIR, FILE_ROUTER, FILE_ROUTER_MERGE, FEATURE_WEB_DATA_COLLECTOR
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
from pipelines.standard_pipeline.packing_pipeline import PackingPipeline
from pipelines.standard_pipeline.loading_pipeline import LoadingPipeline

# remote imports
import sys
import multiprocessing
from pathlib import Path

logger = setup_logger(__name__)

def read_execution_mode(file_path: Path) -> dict:

    config = {}
    with file_path.open('r', encoding='utf-8') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=')
                config[key.strip().upper()] = value.strip()
    return config

def main():
        data_update()

def run_pipeline(pipeline_class, input_path, output_path):
    """
    runs the pipeline with the given class, input path, and output path
    """
    pipeline = pipeline_class()
    pipeline.run(input_path=input_path, output_path=output_path)
    logger.info(f'pipeline {pipeline_class.__name__} finalizado')

t1 = multiprocessing.Process(
    target=data_extraction_olpn_from_file, args=("cookies.json", FEATURE_WEB_DATA_COLLECTOR['BRONZE']['olpn']))
t3 = multiprocessing.Process(
    target=data_extraction_picking_from_file, args=("cookies.json", FEATURE_WEB_DATA_COLLECTOR['BRONZE']['picking']))
t5 = multiprocessing.Process(
    target=data_extraction_packing_from_file, args=("cookies.json", FEATURE_WEB_DATA_COLLECTOR['BRONZE']['packing']))
t6 = multiprocessing.Process(
    target=data_extraction_loading_from_File, args=("cookies.json", FEATURE_WEB_DATA_COLLECTOR['BRONZE']['loading']))

p1 = multiprocessing.Process(
    target=run_pipeline,
    args=(OlpnPipeline, FEATURE_WEB_DATA_COLLECTOR['BRONZE']['olpn'], FEATURE_WEB_DATA_COLLECTOR['SILVER']['olpn']))

p2 = multiprocessing.Process(
    target=run_pipeline,
    args=(PickingPipeline, FEATURE_WEB_DATA_COLLECTOR['BRONZE']['picking'], FEATURE_WEB_DATA_COLLECTOR['SILVER']['picking']))

p5 = multiprocessing.Process(
    target=run_pipeline,
    args=(PackingPipeline, FEATURE_WEB_DATA_COLLECTOR['BRONZE']['packing'], FEATURE_WEB_DATA_COLLECTOR['SILVER']['packing']))

p6 = multiprocessing.Process(
    target=run_pipeline,
    args=(LoadingPipeline, FEATURE_WEB_DATA_COLLECTOR['BRONZE']['loading'], FEATURE_WEB_DATA_COLLECTOR['SILVER']['loading']))

@log_with_context(job='main', logger=logger)
def data_update():

    logger.info('iniciando processo de extracao de dados do csi', extra={
        'job': 'main',
        'status': 'started'
    })

    cookies = login_csi(TEMP_DIR['BRONZE']['dir_chrome_login'])

    if not cookies:
        logger.error('login falhou: cookies nao obtidos. abortando processo', extra={
            'job': 'main',
            'status': 'failed'
        })
        sys.exit(1)

    # for t in [t1,t3,t5,t6]:
    #     t.start()

    # for t in [t1,t3,t5,t6]:
    #     t.join()

    rename_csv_with_yesterday(temp_dir=FEATURE_WEB_DATA_COLLECTOR['BRONZE'])

    logger.info('processos de extracao finalizados, iniciando primeira etapa de pipelines', extra={
        'job': 'main',
        'status': 'pipelines_started'
        })

    for p in [p1, p2, p6]:
        p.start()
    
    for p in [p1, p2, p6]:
        p.join()

    logger.info('primeira etapa dos pipelines finalizada, iniciando segunda etapa de pipelines', extra={
        'job': 'main',
        'status': 'pipelines_started'
        })
    
    for p in [p5]:
        p.start()
    
    for p in [p5]:
        p.join()
    
    logger.info('pipelines finalizados', extra={
        'job': 'main',
        'status': 'success'
        })
    
    merge_parquet(FILE_ROUTER_MERGE)
    
    move_files(FILE_ROUTER)


if __name__ == "__main__":
    main()