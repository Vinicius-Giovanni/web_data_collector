from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from utils.config_logger import log_with_context
from config.pipeline_config import logger

@log_with_context(job='get_yesterday_date', logger=logger)
def get_yesterday_date(format: str = '%d/%m/%Y') -> str:
    """
    returns yesterday's date in the specified format.
    """
    try:
        logger.info('iniciando calculo da data de ontem', extra={
            'job': 'get_yesterday_date',
            'status': 'started'
        })

        yesterday_date = (datetime.now() - timedelta(days=1)).strftime(format)

        logger.info(f'data de ontem calculada: {yesterday_date}', extra={
            'job': 'get_yesterday_date',
            'status': 'success'
        })

        return yesterday_date
    
    except Exception as e:
        logger.exception(f'erro ao calcular data de ontem: {e}', extra={
            'job': 'get_yesterday_date',
            'status': 'failure'
        })
        return None
    
@log_with_context(job='get_penultimate_date', logger=logger)
def get_penultimate_date(parquet_folder: Path, column: str = 'data_criterio', date_format: str = '%d/%m/%Y') -> str | None:
    """
    returns the penultimate date from the parquet files in the specified folder
    """

    all_files = list(parquet_folder.glob('*.parquet'))

    if not all_files:
        logger.warning(f'nenhum arquivo encontrado em {parquet_folder}', extra={
            'job': 'get_penultimate_date',
            'status': 'no_files'
        })
        return None
    

    all_dates = []

    for file in all_files:
        try:
            df = pd.read_parquet(file, columns=[column])
            all_dates.extend(df[column].dropna().tolist())
        except Exception as e:
            logger.critical(f'erro ao ler arquivo {file}', extra={
                'job': 'get_penultimate_date',
                'status': 'file_read_error'
            })
    
    if len(all_dates) < 2:
        logger.warning('menos de duas datas encontradas, nao e possivel determinar a penultima data', extra={
            'job': 'get_penultimate_date',
            'status': 'failure'
        })
        return None
    
    all_dates = pd.to_datetime(all_dates, errors='coerce', dayfirst=True)
    unique_sorted_dates = sorted(set(all_dates), reverse=True)

    penultimate = unique_sorted_dates[0] if len(unique_sorted_dates) > 0 else None
    return penultimate.strftime(date_format) if penultimate else None

def load_penultimate_dates(data_paths: dict, column: str = 'data_criterio', date_format: str = '%d/%m/%Y') -> dict[str, str | None]:
    """
    percorre todos os paths em DATA_PATHS, calcula a penultima data e armazena no dicionario global PENULTIMATE_DATES
    """

    results = {}
    for key, path in data_paths.items():
        results[key] = get_penultimate_date(path, column, date_format)
    return results