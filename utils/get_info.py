from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from utils.config_logger import log_with_context
from config.pipeline_config import logger
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

@log_with_context(job='today', logger=logger)
def today(format: str = '%d/%m/%Y') -> str:
    """
    Retornar a data atual e permite a mudança de formato
    Será usada para o modo de atualização em tempo real
    """
    current_date = datetime.now().strftime(format)

    return current_date

@log_with_context(job='yesterday', logger=logger)
def yesterday(format: str ='%d/%m/%Y') -> str:
    """
    Retornar a data de ontem e permite a mudança de formato
    Será usada para o modo de atualização de histórico
    """
    yesterday_date = (datetime.now() - timedelta(days=1)).strftime(format)

    return yesterday_date

@log_with_context(job='penultimate_date', logger=logger)
def penultimate_date(parquet_folder: Path, column: str = 'data_criterio', format: str = '%d/%m/%Y') -> str | None:
    """
    Retorna a penultima data do datalake
    Será usada para o modo de atualização de histórico
    """
    
    files = list(parquet_folder.glob('*.parquet'))

    if not files:
        logger.critical(f'nao foi possivel calcular a data de atualizacao do DataLake. Path incorreto', extra={'job': 'funcao penultimate_date'})
        return None
    
    dates = []

    for file in files:
        df = pd.read_parquet(file, columns=[column])
        dates.extend(df[column].dropna().tolist())
    
    dates = pd.to_datetime(dates, errors='coerce', dayfirst=True)
    unique = sorted(set(dates), reverse=True)

    penultimate = unique[1] if len(unique) > 0 else None
    
    return penultimate.strftime(format=format) if penultimate else None

@log_with_context(job='business_date', logger=logger)
def business_date(format: str = '%d/%m/%Y') -> str:
    """
    Retorna a data usando a lógica de negócio do online
    """

    today = datetime.now()
    weekday = today.weekday()

    if 1<= weekday <=5:
        target_date = today - timedelta(days=1)
    else:
        days_to_subtract = (weekday - 4) % 7
        target_date = today - timedelta(days=days_to_subtract)

    formatted = target_date.strftime(format=format)

    return formatted