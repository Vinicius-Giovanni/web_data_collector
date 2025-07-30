# remote imports
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# local imports
from utils.config_logger import setup_logger, log_with_context

# %(name)s <<< module name
logger = setup_logger(__name__)

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
def get_penultimate_date(parquet_folder: str, column: str = 'data_criterio', format: str = '%d/%m/%Y') -> str | None:
    """
    returns the penultimate date from the parquet files in the specified folder
    """

    folder_path = Path(parquet_folder)
    all_files = list(folder_path.glob('*.parquet'))

    if not all_files:
        logger.warning(f'nenhum arquivo parquet encontrado em {parquet_folder}', extra={
            'job': 'get_penultimate_date',
            'status': 'no_files'
        })

        raise FileNotFoundError(f'nenhum arquivo parquet encontrado em {folder_path}')
    
    all_dates = []

    for file in all_files:
        # read the parquet file and extract the specified column
        try:
            df = pd.read_parquet(file, columns=[column])
            all_dates.extend(df[column].dropna().tolist())
            logger.info('procurando pela penultima data', extra={
                'job': 'get_penultimate_date',
                'status': 'file_processed',
                'file': str(file)
            })
        except Exception as e:
            logger.critical(f'erro ao ler arquivo {file}: {e}', extra={
                'job': 'get_penultimate_date',
                'status': 'file_read_error',
                'file': str(file)
            })
    
    if len(all_dates) < 2:
        logger.warning('menos de duas datas encontradas, não é possível determinar a penúltima data', extra={
            'job': 'get_penultimate_date',
            'status': 'not_enough_dates'
        })
        return None
    
    all_dates = pd.to_datetime(all_dates, errors='coerce', dayfirst=True)
    unique_sorted_dates = sorted(set(all_dates), reverse=True)

    penultimate = unique_sorted_dates[1] if len(unique_sorted_dates) > 1 else None # <<< acess the second date of the unique_sorted_dates
    return penultimate.strftime(format) if penultimate else None