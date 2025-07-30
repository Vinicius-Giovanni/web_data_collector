# remote imports
import shutil
import os
from pathlib import Path
import time
from typing import Dict

# local imports
from utils.config_logger import setup_logger, log_with_context
from config.settings import FILE_ROUTER


# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='clear_dirs', logger=logger)
def clear_dirs(dirs: Dict[str, Path]) -> None:
    """
    clear the directories specified in the dict. If not present, they are created.
    """
    logger.info(f'iniciando limpeza dos diretorios: {list(dirs.keys())}', extra={
        'job': 'clear_dirs',
        'status': 'started'
    })

    for name, folder in dirs.items():
        try:
            if not folder.exists():
                logger.warning(f'diretorio {name} ({folder}) nao existe. criando...', extra={
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
                    logger.exception(f'erro ao remover {item} em {name} ({folder}): {e}', extra={
                        'job': 'clear_dirs',
                        'status': 'failure'
                    })

            logger.info(f'Diretório {name} ({folder}) limpo com sucesso.', extra={
                'job': 'clear_dirs',
                'status': 'success'
            })

        except Exception as e:
            logger.exception(f'erro ao processar diretorio {name} ({folder}): {e}', extra={
                'job': 'clear_dirs',
                'status': 'failure'
            })

@log_with_context(job='wait_download_csv', logger=logger)
def wait_download_csv(dir: str | Path,
                      timeout: int = 300,
                      poll: float = 2.0,
                      stable_cheks: int = 3) -> bool:
    
    """
    - ignores pre-existing files in the directory
    - avoids processing files that are still being downloaded (via .crdownload)
    - checks whether the file size has stabilized, ensuring the file was completely whitten
    - transient fault tolerance with multiple attempts before considering a timeout
    """
    
    dir_path = Path(dir)

    logger.info(f'aguardando download do csv em {dir_path}', extra={
        'job': 'wait_download_csv',
        'status': 'started'
    })

    t0 = time.time()
    baseline = {f.name for f in dir_path.glob('*.csv')}

    candidate: Path | None = None
    stable_couter = 0
    last_size = -1

    while time.time() - t0 < timeout:
        new_csvs = [f for f in dir_path.glob('*.csv') if f.name not in baseline]

        if new_csvs:
            candidate = max(new_csvs, key=lambda f: f.stat().st_mtime)

            if (candidate.with_suffix(candidate.suffix + '.crdownload')).exists():
                stable_couter = 0
            else:
                size_now = candidate.stat().st_size
                if size_now == last_size and size_now > 0:
                    stable_couter += 1
                else:
                    stable_couter = 0
                last_size = size_now
            if stable_couter >= stable_cheks:
                logger.info(f'arquivo {candidate.name} ({size_now:,}) bytes baixado com sucesso', extra={
                    'job': 'wait_download_csv',
                    'status': 'success'
                })

                return True
            
        time.sleep(poll)
    
    logger.warning(f'tempo limite de {timeout} segundos atingido sem encontrar um arquivo csv estavel', extra={
        'job': 'wait_download_csv',
        'status': 'timeout'
    })

@log_with_context(job='function_distribution', logger=logger)
def function_distribution(path_folder: Path):
    """
    - searches for specific strings within the .csv file names within the directory
        - add a dict with the searched strings
        - call the specific pipeline for the file, sending the file path as a parameter
    """

    for file in path_folder.iterdir():
        if file.is_file() and file.suffix == '.csv':
            for key, pipeline_func in FILE_ROUTER.items():
                if key in file.name:
                    pipeline_func(path=file)
                    break