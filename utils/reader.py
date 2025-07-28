# remote imports
import shutil
import os
from pathlib import Path
import time
from typing import Dict
import pandas as pd

# local imports
from utils.config_logger import setup_logger, log_with_context
from config.settings import TEMP_DIR

# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='clear_dirs')
def clear_dirs(dirs: Dict[str, Path]) -> None:
    """
    clear the directories specified in the dict.
    """

    logger.info(f'iniciando limpeza no di {dirs}', extra={
        'job': 'clear_dirs',
        'status': 'started'
    })

    for name, folder in dirs.items():
        try:
            if not folder.exists():
                logger.warning(f'diretorio {folder} nao existe, iniciando criacao de novo diretorio', extra={
                'job': 'clear_dirs',
                })
                folder.mkdir(parents=True, exist_ok=True)
                continue

            for item in folder.iterdir():
                try:
                    if item.is_file() or item.is_symlink():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    logger.exception(f'erro ao limpar {item} na pasta {folder}: {e}', extra={
                        'job': 'clear_dirs',
                        'status': 'failure'
                    })
        except Exception as e:
            logger.exception(f'erro ao limpar {folder}: {e}', extra={
                'job': 'clear_dirs',
                'status': 'failure'
            })

    logger.info(f'diretorio {folder} limpo com sucesso', extra={
        'job': 'clear_dirs',
        'status': 'success'
    })
                
