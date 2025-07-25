# remote imports
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# local imports
from utils.config_logger import setup_logger, log_with_context

# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='get_yesterday_date')
def get_yesterday_date(format: str = '%d/%m/%Y', logger=None) -> str:
    """
    returns yesterday's date in the specified format.
    """
    try:
        logger.info('iniciando cálculo da data de ontem', extra={
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