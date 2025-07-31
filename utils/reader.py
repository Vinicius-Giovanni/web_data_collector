# remote imports
import shutil
import pandas as pd
from pathlib import Path
import time
from typing import Dict
import os
import shutil

# local imports
from utils.config_logger import setup_logger, log_with_context
from config.settings import CHUNKSIZE, PIPELINE_CONFIG

# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='clear_dirs', logger=logger)
def clear_dirs(dirs: Dict[str, any], prefix: str = '') -> None:
    """
    clear the directories specified in the dict. If not present, they are created.
    """
    for name, folder in dirs.items():
        full_name = f'{prefix}_{name}' if prefix else name

        if isinstance(folder, dict):
            clear_dirs(folder, prefix=full_name)
            continue
        
        try:
            if not folder.exists():
                logger.warning(f'diretorio {full_name} ({folder}) nao existe. criando...', extra={
                    'job': 'clear_dirs',
                    'status': 'creating folders'
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
                    logger.exception(f'erro ao remover {item} em {full_name} ({folder})', extra={
                        'job': 'clear_dirs',
                        'status': 'failure'
                    })
            logger.info(f'diretorio {full_name} ({folder}) limpo', extra={
                'job': 'clear_dirs',
                'status': 'success'
            })
        
        except Exception as e:
            logger.exception(f'erro ao processar diretorio {full_name} ({folder})', extra={
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

@log_with_context(job='read_csv', logger=logger)
def read_csv(path: Path, pipeline_key: str) -> pd.DataFrame:

    logger.info(f'leitura arquivo: {path} pipeline: {pipeline_key}', extra={
        'job': 'read_csv',
        'status': 'started'
    })

    cfg = PIPELINE_CONFIG.get(pipeline_key)
    if not cfg:
        logger.critical(f'pipeline {pipeline_key} invalido', extra={
            'job': 'read_csv',
            'status': 'failure'
        })
        return pd.DataFrame()
    
    # Caso a conf do arquivo não existe, define como padrão o utf-8 e o separador ;
    encoding = cfg.get('encoding', 'utf-8')
    sep = cfg.get('sep', ';')

    dataframes = []

    if path.is_file() and path.suffix == '.csv':
        files = [path]
    elif path.is_dir():
        files = list(path.glob('*.csv'))
    else:
        logger.critical(f'caminho {path} nao e um arquivo ou diretorio valido', extra={
            'job': 'read_csv',
            'status': 'failure'
        })
        return pd.DataFrame()
    
    for file in files:
        try:
            for chunk in pd.read_csv(
                file,
                encoding=encoding,
                sep=sep,
                chunksize=CHUNKSIZE,
                low_memory=False,
            ):
                dataframes.append(chunk)
        except Exception as e:
            logger.error(f'erro ao ler arquivo {file}: {e}', extra={
                'job': 'read_csv',
                'status': 'failure'
            })

    return pd.concat(dataframes, ignore_index=True) if dataframes else pd.DataFrame()

@log_with_context(job='export_as_parquet', logger=logger)
def export_as_parquet(df: pd.DataFrame, output_folder: Path, pipeline_key: str, name: str):
    cfg = PIPELINE_CONFIG.get(pipeline_key)
    if not cfg:
        logger.critical(f'pipeline "{pipeline_key}" nao encontrado nas configuracoes', extra={
            'job': 'export_as_parquet',
            'status': 'failure'
        })
        return
    
    output_file = output_folder/ f'{name}.parquet'

    try:
        df.to_parquet(output_file, index=False)
        logger.info(f'sucesso ao exportar: {output_file.name} ({len(df):,} linhas)'.replace(',','.'))
    except Exception as e:
        logger.critical(f'erro ao exportar para parquet: {e}')

@log_with_context(job='forward_files_by_name', logger=logger)
def forward_files_by_name(input_folder: Path, file_router: dict):
    """
    - movs files from a source folder to specific destinations basead on their name as defined
      in the routing dictionary
    - case-insensitive
    """

    if not os.path.isdir(input_folder):
        logger.critical(f'diretorio informado nao existe: {input_folder}', extra={
            'job': 'forward_files_by_name',
            'status': 'failure'
        })
        raise ValueError
    
    files = os.listdir(input_folder)

    for file in files:
        file_lower = file.lower()
        match_found = False

        for route_key, destination in file_router.items():
            if route_key.lower() in file_lower:
                match_found = True

                if not destination:
                    logger.critical(f'sem destino definido para "{route_key}"', extra={
                        'job': 'forward_files_by_name',
                        'status': 'continue'
                    })
                    break

                path_origin = os.path.join(input_folder, file)
                path_destination = os.path.join(destination, file)
                
                os.makedirs(destination, exist_ok=True)
                shutil.move(path_origin, path_destination)

                logger.info(f'"{file}" movido -> "{destination}"', extra={
                    'job': 'forward_files_by_name',
                    'status': 'success'
                })
                break

        if not match_found:
            logger.info(f'"{file}" ignorado por nao conter nenhum padrao de FILE_ROUTER', extra={
                'job': 'forward_files_by_name',
                'status': 'skipped'
            })