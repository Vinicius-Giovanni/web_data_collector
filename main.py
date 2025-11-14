from web_data_collector.login import login_csi
from config.paths import TEMP_DIR, REAL_TIME_UPDATE, DATA_PATHS, FILE_ROUTER_MERGE, FILE_ROUTER
import multiprocessing
from web_data_collector.olpn import data_extraction_olpn_from_file
from web_data_collector.picking import data_extraction_picking_from_file
from web_data_collector.packing import data_extraction_packing_from_file
from web_data_collector.loading import data_extraction_loading_from_File
from web_data_collector.putaway import data_extraction_putaway_from_file
from web_data_collector.cancel import data_extraction_cancel_from_file
from web_data_collector.expedicao_cd import data_extraction_expedicao_from_file
from extracao_recebimento.movimentacao_estoque import data_extraction_mov_estoque_from_file
from extracao_recebimento.pendencia_asn import data_extraction_pendencia_asn_from_file
from extracao_recebimento.recebimento import data_extraction_recebimento_from_file
from utils.reader import rename_csv, merge_parquet, move_files
from pipelines.standard_pipeline.olpn_pipeline import OlpnPipeline
from pipelines.standard_pipeline.picking_pipeline import PickingPipeline
from pipelines.standard_pipeline.cancel_pipeline import CancelPipeline
from pipelines.standard_pipeline.putaway_pipeline import PutawayPipeline
from pipelines.standard_pipeline.packing_pipeline import PackingPipeline
from pipelines.standard_pipeline.loading_pipeline import LoadingPipeline
from pipelines.standard_pipeline.expedicao_cd_pipeline import ExpedicaoPipeline
from config.pipeline_config import logger
from utils.get_info import today, yesterday, penultimate_date
from pipelines.specific_analysis.bottleneck_box import BottleneckBoxPipeline
from pipelines.specific_analysis.time_lead_olpn import TimeLeadOLPNPipeline
from pipelines.specific_analysis.bottleneck_salao import BottleneckSalaoPipeline
from pipelines.specific_analysis.jornada_pipeline import JornadaPipeline

def run(pipeline_class, input_path, output_path):
    pipeline = pipeline_class()
    pipeline.run(input_path=input_path, output_path=output_path)

def update_database_no_reload():
    "update for dabase"

    yesterdays = yesterday()
    
    cookies = login_csi(TEMP_DIR['BRONZE']['dir_chrome_login'])

    if not cookies:
        logger.critical('Login falhou, cookies não obtidos.')

    instance_1 = multiprocessing.Process(
        target=data_extraction_olpn_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['olpn'],
            "parquet_folder": DATA_PATHS['gold']['olpn'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['olpn']),
            "list_filial": ["1200"]
        }
    )
    instance_2 = multiprocessing.Process(
        target = data_extraction_picking_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['picking'],
            "parquet_folder": DATA_PATHS['gold']['picking'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['picking']),
            "list_filial": ["1200"]
        }
    )
    
    instance_3 = multiprocessing.Process(
        target = data_extraction_packing_from_file,
        kwargs={
            'cookies_path':"cookies.json",
            'download_dir':TEMP_DIR['BRONZE']['packing'],
            'parquet_folder':TEMP_DIR['GOLD']['packing'],
            'entry_date':yesterday(format='%b %Y'),
            'exit_date':penultimate_date(parquet_folder=DATA_PATHS['gold']['packing'], format='%b %Y'),
            'list_filial':['1200'],
            'id_data_entry':penultimate_date(parquet_folder=DATA_PATHS['gold']['packing']),
            'id_exit_data':yesterdays
        }
    )
    instance_4 = multiprocessing.Process(
        target = data_extraction_loading_from_File,
        kwargs={
            'cookies_path':"cookies.json",
            'download_dir':TEMP_DIR['BRONZE']['loading'],
            'parquet_folder':TEMP_DIR['GOLD']['loading'],
            'entry_date':yesterday(format='%b %Y'),
            'exit_date':penultimate_date(parquet_folder=DATA_PATHS['gold']['loading'], format='%b %Y'),
            'list_filial':['1200'],
            'id_data_entry':penultimate_date(parquet_folder=DATA_PATHS['gold']['loading']),
            'id_exit_data':yesterdays
        }
    )
    instance_5 = multiprocessing.Process(
        target = data_extraction_putaway_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['putaway'],
            "parquet_folder": DATA_PATHS['gold']['putaway'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['putaway']),
            "list_filial": ["1200"]
        }
    )
    instance_6 = multiprocessing.Process(
        target = data_extraction_cancel_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['cancel'],
            "parquet_folder": DATA_PATHS['gold']['cancel'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['cancel']),
            "list_filial": ["1200"]
        }
    )
    instance_7 = multiprocessing.Process(
        target = data_extraction_expedicao_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['expedicao'],
            "parquet_folder": DATA_PATHS['gold']['expedicao'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['expedicao']),
            "list_filial": ["1200"]
        }
    )

    for process in [instance_1, instance_2, instance_3, instance_4, instance_5, instance_6]:
        process.start()
    for process in [instance_1, instance_2, instance_3, instance_4, instance_5, instance_6]:
        process.join()
    
    rename_csv(path=TEMP_DIR['BRONZE'])

def reread_database():
    "reread database"

    pipeline_1= multiprocessing.Process(
        target=run,
        args=(OlpnPipeline, DATA_PATHS['bronze']['olpn'], DATA_PATHS['gold']['olpn']))
    pipeline_2= multiprocessing.Process(
        target=run,
        args=(PickingPipeline, DATA_PATHS['bronze']['picking'], DATA_PATHS['gold']['picking']))
    pipeline_4= multiprocessing.Process(
        target=run,
        args=(LoadingPipeline, DATA_PATHS['bronze']['loading'], DATA_PATHS['gold']['loading']))
    pipeline_5= multiprocessing.Process(
        target=run,
        args=(PutawayPipeline, DATA_PATHS['bronze']['putaway'], DATA_PATHS['gold']['putaway']))
    pipeline_6= multiprocessing.Process(
        target=run,
        args=(CancelPipeline, DATA_PATHS['bronze']['cancel'], DATA_PATHS['gold']['cancel']))
    pipeline_7= multiprocessing.Process(
        target=run,
        args=(ExpedicaoPipeline, DATA_PATHS['bronze']['expedicao'], DATA_PATHS['gold']['expedicao']))
    
    for pipelines in [pipeline_1]:
        pipelines.start()
    for pipelines in [pipeline_1]:
        pipelines.join()

    for pipelines in [pipeline_2]:
        pipelines.start()
    for pipelines in [pipeline_2]:
        pipelines.join()

    for pipelines in [pipeline_4]:
        pipelines.start()
    for pipelines in [pipeline_4]:
        pipelines.join()

    for pipelines in [pipeline_5]:
        pipelines.start()
    for pipelines in [pipeline_5]:
        pipelines.join()

    for pipelines in [pipeline_6]:
        pipelines.start()
    for pipelines in [pipeline_6]:
        pipelines.join()

    for pipelines in [pipeline_7]:
        pipelines.start()
    for pipelines in [pipeline_7]:
        pipelines.join()
    
    pipeline_3= multiprocessing.Process(
    target=run,
    args=(PackingPipeline, DATA_PATHS['bronze']['packing'], DATA_PATHS['silver']['packing']))

    for pipelines in [pipeline_3]:
        pipelines.start()
    for pipelines in [pipeline_3]:
        pipelines.join()

    merge_parquet(FILE_ROUTER_MERGE)
    move_files(FILE_ROUTER)

    bottleneck_box_pipeline = BottleneckBoxPipeline()
    df_bottleneck_box_pipeline = bottleneck_box_pipeline.run()
    if not df_bottleneck_box_pipeline.empty:
        print('Pipeline executado com sucesso.')

    bottleneck_salao_pipeline = BottleneckSalaoPipeline()
    df_bottleneck_salao_pipeline = bottleneck_salao_pipeline.run()
    if not df_bottleneck_salao_pipeline.empty:
        print('Pipeline executado com sucesso.')

    time_lead = TimeLeadOLPNPipeline()
    df_time_lead = time_lead.run()
    if not df_time_lead.empty:
        print('Pipeline executado com sucesso.')

    jornada_pipeline = JornadaPipeline()
    df_jornada_pipeline = jornada_pipeline.run()
    if not df_jornada_pipeline.empty:
        print('Pipeline executado com sucesso.')


def database_update():
    "update for dabase"

    yesterdays = yesterday()
    
    cookies = login_csi(TEMP_DIR['BRONZE']['dir_chrome_login'])

    if not cookies:
        logger.critical('Login falhou, cookies não obtidos.')

    instance_1 = multiprocessing.Process(
        target=data_extraction_olpn_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['olpn'],
            "parquet_folder": DATA_PATHS['gold']['olpn'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['olpn']),
            "list_filial": ["1200"]
        }
    )
    instance_2 = multiprocessing.Process(
        target = data_extraction_picking_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['picking'],
            "parquet_folder": DATA_PATHS['gold']['picking'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['picking']),
            "list_filial": ["1200"]
        }
    )
    
    instance_3 = multiprocessing.Process(
        target = data_extraction_packing_from_file,
        kwargs={
            'cookies_path':"cookies.json",
            'download_dir':TEMP_DIR['BRONZE']['packing'],
            'parquet_folder':TEMP_DIR['GOLD']['packing'],
            'entry_date':penultimate_date(parquet_folder=DATA_PATHS['gold']['packing'], format='%b %Y'),
            'exit_date':yesterday(format='%b %Y'),
            'list_filial':['1200'],
            'id_data_entry':penultimate_date(parquet_folder=DATA_PATHS['gold']['packing']),
            'id_exit_data':yesterdays
        }
    )
    instance_4 = multiprocessing.Process(
        target = data_extraction_loading_from_File,
        kwargs={
            'cookies_path':"cookies.json",
            'download_dir':TEMP_DIR['BRONZE']['loading'],
            'parquet_folder':TEMP_DIR['GOLD']['loading'],
            'entry_date':penultimate_date(parquet_folder=DATA_PATHS['gold']['loading'], format='%b %Y'),
            'exit_date':yesterday(format='%b %Y'),
            'list_filial':['1200'],
            'id_data_entry':penultimate_date(parquet_folder=DATA_PATHS['gold']['loading']),
            'id_exit_data':yesterdays
        }
    )
    instance_5 = multiprocessing.Process(
        target = data_extraction_putaway_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['putaway'],
            "parquet_folder": DATA_PATHS['gold']['putaway'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['putaway']),
            "list_filial": ["1200"]
        }
    )
    instance_6 = multiprocessing.Process(
        target = data_extraction_cancel_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['cancel'],
            "parquet_folder": DATA_PATHS['gold']['cancel'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['cancel']),
            "list_filial": ["1200"]
        }
    )
    instance_7 = multiprocessing.Process(
        target = data_extraction_expedicao_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['expedicao'],
            "parquet_folder": DATA_PATHS['gold']['expedicao'],
            "entry_date": yesterdays,
            "exit_date": penultimate_date(parquet_folder=DATA_PATHS['gold']['expedicao']),
            "list_filial": ["1200"]
        }
    )

    for process in [ instance_1, instance_2, instance_3, instance_4, instance_5, instance_6, instance_7]:
        process.start()
    for process in [ instance_1, instance_2, instance_3, instance_4, instance_5, instance_6, instance_7]:
        process.join()
    
    rename_csv(path=TEMP_DIR['BRONZE'])

    pipeline_1= multiprocessing.Process(
        target=run,
        args=(OlpnPipeline, TEMP_DIR['BRONZE']['olpn'], DATA_PATHS['silver']['olpn']))
    pipeline_2= multiprocessing.Process(
        target=run,
        args=(PickingPipeline, TEMP_DIR['BRONZE']['picking'], DATA_PATHS['silver']['picking']))
    pipeline_4= multiprocessing.Process(
        target=run,
        args=(LoadingPipeline, TEMP_DIR['BRONZE']['loading'], DATA_PATHS['silver']['loading']))
    pipeline_5= multiprocessing.Process(
        target=run,
        args=(PutawayPipeline, TEMP_DIR['BRONZE']['putaway'], DATA_PATHS['silver']['putaway']))
    pipeline_6= multiprocessing.Process(
        target=run,
        args=(CancelPipeline, TEMP_DIR['BRONZE']['cancel'], DATA_PATHS['silver']['cancel']))
    pipeline_7= multiprocessing.Process(
        target=run,
        args=(ExpedicaoPipeline, TEMP_DIR['BRONZE']['expedicao'], DATA_PATHS['silver']['expedicao']))

    for pipelines in [pipeline_1, pipeline_2, pipeline_4, pipeline_5, pipeline_6, pipeline_7]:
        pipelines.start()
    for pipelines in [pipeline_1, pipeline_2, pipeline_4, pipeline_5, pipeline_6, pipeline_7]:
        pipelines.join()
    
    pipeline_3= multiprocessing.Process(
    target=run,
    args=(PackingPipeline, TEMP_DIR['BRONZE']['packing'], DATA_PATHS['silver']['packing']))

    for pipelines in [pipeline_3]:
        pipelines.start()
    for pipelines in [pipeline_3]:
        pipelines.join()
    
    merge_parquet(FILE_ROUTER_MERGE)
    move_files(FILE_ROUTER)

    bottleneck_box_pipeline = BottleneckBoxPipeline()
    df_bottleneck_box_pipeline = bottleneck_box_pipeline.run()
    if not df_bottleneck_box_pipeline.empty:
        print('Pipeline executado com sucesso.')

    bottleneck_salao_pipeline = BottleneckSalaoPipeline()
    df_bottleneck_salao_pipeline = bottleneck_salao_pipeline.run()
    if not df_bottleneck_salao_pipeline.empty:
        print('Pipeline executado com sucesso.')

    time_lead = TimeLeadOLPNPipeline()
    df_time_lead = time_lead.run()
    if not df_time_lead.empty:
        print('Pipeline executado com sucesso.')

    jornada_pipeline = JornadaPipeline()
    df_jornada_pipeline = jornada_pipeline.run()
    if not df_jornada_pipeline.empty:
        print('Pipeline executado com sucesso.')


def real_time_update():
    "update for real time"

    cookies = login_csi(TEMP_DIR['BRONZE']['dir_chrome_login'])

    instance_1 = multiprocessing.Process(
        target=data_extraction_olpn_from_file, args=("cookies.json", REAL_TIME_UPDATE['BRONZE']['olpn'])
    )
    instance_2 = multiprocessing.Process(
        target = data_extraction_picking_from_file, args=("cookies.json", REAL_TIME_UPDATE['BRONZE']['picking'])
    )
    instance_3 = multiprocessing.Process(
        target = data_extraction_packing_from_file, args=("cookies.json", REAL_TIME_UPDATE['BRONZE']['packing'])
    )
    instance_4 = multiprocessing.Process(
        target = data_extraction_loading_from_File, args=("cookies.json", REAL_TIME_UPDATE['BRONZE']['loading'])
    )
    instance_5 = multiprocessing.Process(
        target = data_extraction_putaway_from_file, args=("cookies.json", REAL_TIME_UPDATE['BRONZE']['putaway'])
    )

    pipeline_1= multiprocessing.Process(
        target=run,
        args=(OlpnPipeline, REAL_TIME_UPDATE['BRONZE']['olpn'], REAL_TIME_UPDATE['SILVER']['olpn']))
    pipeline_2= multiprocessing.Process(
        target=run,
        args=(PickingPipeline, REAL_TIME_UPDATE['BRONZE']['picking'], REAL_TIME_UPDATE['SILVER']['picking']))
    pipeline_4= multiprocessing.Process(
        target=run,
        args=(LoadingPipeline, REAL_TIME_UPDATE['BRONZE']['loading'], REAL_TIME_UPDATE['SILVER']['loading']))
    pipeline_5= multiprocessing.Process(
        target=run,
        args=(PutawayPipeline, REAL_TIME_UPDATE['BRONZE']['putaway'], REAL_TIME_UPDATE['SILVER']['putaway']))
    
    for pipelines in [pipeline_1, pipeline_2, pipeline_4, pipeline_5]:
        pipelines.start()
    for pipelines in [pipeline_1, pipeline_2, pipeline_4, pipeline_5]:
        pipelines.join()
    
    pipeline_3= multiprocessing.Process(
    target=run,
    args=(PackingPipeline, REAL_TIME_UPDATE['BRONZE']['packing'], REAL_TIME_UPDATE['SILVER']['packing']))

    for pipelines in [pipeline_3]:
        pipelines.start()
    for pipelines in [pipeline_3]:
        pipelines.join()
    
    for process in [instance_1, instance_2, instance_3, instance_4, instance_5]:
        process.start()
    for process in [instance_1, instance_2, instance_3, instance_4, instance_5]:
        process.join()

    rename_csv(path=REAL_TIME_UPDATE['BRONZE'])

def teste():

    todays = today()

    yesterdays = yesterday()
    
    cookies = login_csi(TEMP_DIR['BRONZE']['dir_chrome_login'])

    if not cookies:
        logger.critical('Login falhou, cookies não obtidos.')

    instance_0 = multiprocessing.Process(
        target=data_extraction_recebimento_from_file,
        kwargs={
            "cookies_path": "cookies.json",
            "download_dir": TEMP_DIR['BRONZE']['recebimento'],
            "parquet_folder": DATA_PATHS['gold']['recebimento'],
            "entry_date": yesterdays,
            "exit_date": todays,
            "list_filial": ["1200"]
        }
    )

    for process in [instance_0]:
        process.start()
    for process in [instance_0]:
        process.join()

    rename_csv(path=TEMP_DIR['BRONZE'])

    move_files(FILE_ROUTER)

def main():
    teste()
    
if __name__ == "__main__":
    main()