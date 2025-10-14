import shutil
import pandas as pd
from pathlib import Path
import time
from typing import Dict
import shutil
import re
from typing import Union, Tuple
from unidecode import unidecode
from datetime import datetime, timedelta
import shutil
from utils.config_logger import log_with_context
from config.pipeline_config import logger, CHUNKSIZE, PIPELINE_CONFIG
from config.regras_de_negocio import MOTIVOS_OFICIAIS, MAPEAMENTO_TEXTUAL, REGRAS_DIRETAS

@log_with_context(job='move_files',logger=logger)
def move_files(path: dict):
    """
    Move files from source (keys) to destination (values) according to the file_router dictionary
    """

    for src_dir, dest_dir in path.items():
        src_dir = Path(src_dir)
        dest_dir = Path(dest_dir)

        dest_dir.mkdir(parents=True, exist_ok=True)

        for file in src_dir.glob('*.*'):
            dest_path = dest_dir / file.name
            shutil.move(str(file), str(dest_path))
            logger.info(f'movendo {file.name} de {src_dir} para {dest_dir}', extra={
                'job': 'move_files',
                'status': 'success'
            })

@log_with_context(job='merge_parquet', logger=logger)
def merge_parquet(path: dict):
    for src_dir, dest_ir in path.items():
        src_dir = Path(src_dir)
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

        dfs = []

        dest_files = list(dest_dir.glob('*.parquet'))
        for f in dest_files:
            dfs.append(pd.read_parquet(f))

        src_files = list(src_dir.glob('*.parquet'))
        for f in src_files:
            dfs.append(pd.read_parquet(f))

        if not dfs:
            logger.info(f'nenhum arquivo parquet encontrado em {src_dir} ou {dest_dir}. pulando...', extra={
                'job': 'merge_parquet',
                'status': 'skipped'
            })
            continue

        merge_df = pd.concat(dfs, ignore_index=True)

        output_file = dest_dir / f'{src_dir.name}_consolidated.parquet'

        merge_df.to_parquet(output_file, index=False)

        for f in dest_files:
            if f != output_file:
                f.unlink()
        
        logger.info(f'merge concluido: {len(src_files)} arquivos da origem + {len(dest_files)} arquivos do destino -> {output_file.name} ({len(merge_df)} registros)',
                    extra={
                'job': 'merge_parquet',
                'status': 'success'
            })

@log_with_context(job='rename_csv', logger=logger)
def rename_csv(path: dict):
    """
    Rename CSV files, add yesterday to the file name
    """
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')

    for key, dir_path in path.items():
        for file in Path(dir_path).glob('*.csv'):
            new_name = file.stem + f'_{yesterday}' + file.suffix
            new_path = file.with_name(new_name)

            file.rename(new_path)

            logger.info(f'arquivo {file.name} renomeado para {new_name}', extra={
                'job': 'rename_csv',
                'status': 'success'
            })

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

    """
    read CSV files from a given path
    """

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

    """
    export a DataFrame to a parquet file
    """

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
        logger.info(f'sucesso ao exportar: {output_file.name} ({len(df):,} linhas) para I{output_folder}I'.replace(',','.'))
    except Exception as e:
        logger.critical(f'erro ao exportar para parquet: {e}')

def normalizar_motivo(valor: Union[str, float]) -> Tuple[int, str]:

    """
    Normalize the cancellation reason for the 'cancel' file
    """
    try:
        if pd.isna(valor) or str(valor).strip() =='':
            return 1, MOTIVOS_OFICIAIS[1]
        
        valor = unidecode(str(valor).lower().strip())
        valor = re.sub(r'[^\w\s]','',valor)

        if valor.isdigit():
            codigo = int(valor)
            if codigo in MOTIVOS_OFICIAIS:
                return codigo, MOTIVOS_OFICIAIS[codigo]
            
        for codigo, must_have, *optional in REGRAS_DIRETAS:
            if all(term in valor for term in must_have):
                if not optional or any(opt in valor for opt in optional[0]):
                    return codigo, MOTIVOS_OFICIAIS[codigo]
        
        for codigo, padroes in MAPEAMENTO_TEXTUAL.items():
            if any(re.search(p, valor) for p in padroes):
                return codigo, MOTIVOS_OFICIAIS[codigo]
        
        return 1,MOTIVOS_OFICIAIS[1]
    except Exception as e:
        logger.warning(f"Erro ao normalizar motivo '{valor}': {e}")
        return 1, MOTIVOS_OFICIAIS[1]

@log_with_context(job='read_parquet_with_tote', logger=logger)
def read_parquet_with_tote(folder: Path) -> pd.DataFrame:

    """
    reading specific columns of parquet files
    """

    dataframes = []
    for file in folder.glob('*.parquet'):
        try:
            df = pd.read_parquet(file, columns=['olpn', 'tote'])
            dataframes.append(df)
        except Exception as e:
            logger.warning(f'erro ao ler {file.name}', extra={
                'job': 'read_parquet_with_tote',
                'status': 'failure'
            })

    return pd.concat(dataframes, ignore_index=True).drop_duplicates(subset='olpn') if dataframes else pd.DataFrame()

@log_with_context(job='rename_csv_with_yesterday', logger=logger)
def rename_csv_with_yesterday(temp_dir: dict):
    """
    renames CSV files witin the directories specified in the temp_dir dictionary
    adds yesterday's date to the file name before the extension
    """

    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

    for key, dir_path in temp_dir.items():
        for file in Path(dir_path).glob('*.csv'):
            new_name = file.stem + f'_{yesterday}' + file.suffix
            new_path = file.with_name(new_name)

            file.rename(new_path)
            logger.info(f'arquivo {file.name} renomeado para {new_name}', extra={
                'job': 'rename_csv_with_yesterday',
                'status': 'success'
            })

@log_with_context(job='move_files', logger=logger)
def move_files(file_router: dict):
    """
    Move files from source (keys) to destination (values) according to the file_router dictionary
    """

    for src_dir, dest_dir in file_router.items():
        src_dir = Path(src_dir)
        dest_dir = Path(dest_dir)

        dest_dir.mkdir(parents=True, exist_ok=True)

        for file in src_dir.glob('*.*'):
            dest_path = dest_dir / file.name
            shutil.move(str(file), str(dest_path))
            logger.info(f'movendo {file.name} de {src_dir} para {dest_dir}', extra={
                'job': 'move_files',
                'status': 'success'
            })

@log_with_context(job='merge_parquet', logger=logger)
def merge_parquet(file_router_merge: dict):

    """
    merge all parquet files from the source and destination, ensuring that only one consolidated 
    parquet file reimains at the destination
    """
    for src_dir, dest_dir in file_router_merge.items():
        src_dir = Path(src_dir)
        dest_dir = Path(dest_dir)
        dest_dir.mkdir(parents=True, exist_ok=True)

        dfs = []

        # load files destination
        dest_files = list(dest_dir.glob('*.parquet'))
        for f in dest_files:
            dfs.append(pd.read_parquet(f))
        
        # load files source
        src_files = list(src_dir.glob('*.parquet'))
        for f in src_files:
            dfs.append(pd.read_parquet(f))

        # if there are no files, skip
        if not dfs:
            logger.info(f'nenhum arquivo parquet encontrado em {src_dir} ou {dest_dir}. pulando...', extra={
                'job': 'merge_parquet',
                'status': 'skipped'
            })
            continue

        # all concatenate
        merge_df = pd.concat(dfs, ignore_index=True)

        # rename file
        output_file = dest_dir / f'{src_dir.name}_consolidated.parquet'

        # save consolidate
        merge_df.to_parquet(output_file, index=False)

        # remove old files
        for f in dest_files:
            if f != output_file:
                f.unlink()

        logger.info(f'merge concluido: {len(src_files)} arquivos da origem + {len(dest_files)} arquivos do destino -> {output_file.name} ({len(merge_df)} registros)',
                    extra={
                'job': 'merge_parquet',
                'status': 'success'
            })

def read_parquet_files(self, folder: Path) -> pd.DataFrame:
    dfs = []
    for file in folder.rglob('*.parquet'):
        try:
            df = pd.read_parquet(file, columns=self.cfg['read_columns'])
            dfs.append(df)
            logger.info(f'Lido: {file.name}')
        except Exception as e:
            logger.warning(f'Erro ao ler {file.name}: {e}')
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def read_parquet_folder_columns(self, folder_path: Path, columns: list[str]) -> pd.DataFrame:
    dfs = []
    for file in Path(folder_path).rglob('*.parquet'):
        try:
            df = pd.read_parquet(file, columns=columns)
            dfs.append(df)
            logger.info(f'Lido: {file.name}')
        except Exception as e:
            logger.warning(f'Erro ao ler {file.name}: {e}')
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()