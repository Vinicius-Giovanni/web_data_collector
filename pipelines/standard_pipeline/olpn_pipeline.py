# remote imports
import os
import glob
from pathlib import Path
import pandas as pd
import numpy as np

# local imports
from config.settings import PIPELINE_CONFIG
from utils.config_logger import setup_logger, log_with_context
from utils.classification import classify_setores, check_deadline
from utils.reader import read_csv, export_as_parquet

# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='OlpnPipeline', logger=logger)
class OlpnPipeline:
    #* Flow
    #* raw layer
    #*  raw file (TEMP_DIR['DIR_CHROME_BRONZE'])
    #* silver layer
    #*  reading and cleaning
    #*  save as .parquet (TEMP_DIR['DIR_TEMP_SILVER'])
    #* gold layer
    #*  silver incremental .parquet
    #*  the existing consolidated .parquet

    def __init__(self):
        self.key = 'olpn'
        self.cfg = PIPELINE_CONFIG.get(self.key)

        if not self.cfg:
            logger.critical(f'pipeline {self.key} invalido')
            raise ValueError(f'pipeline {self.key} invalido')
        
    def run(self, input_path: Path, output_path: Path) -> pd.DataFrame:
        """
        run OlpnPipeline
        """

        logger.info(f'Iniciando pipeline {self.key}', extra={
            'job': 'OlpnPipeline',
            'status': 'started'
        })

        input_path.mkdir(parents=True, exist_ok=True)
        output_path.mkdir(parents=True, exist_ok=True)

        df = read_csv(
            path=input_path,
            pipeline_key=self.key
        )

        if df.empty:
            logger.critical('nenhum dado no dataframe', extra={
                'job': 'OlpnPipeline',
                'status': 'failure'
            })
            return pd.DataFrame()

        df = self.preprocess(df)

        if 'mes_ano' not in df.columns:
            logger.critical('coluna "mes_ano" ausente', extra={
                'job': 'OlpnPipene',
                'status': 'failure'
            })

        export_as_parquet(df, output_folder=output_path, pipeline_key=self.key ,name='3.11 - Status Wave + oLPN')

        logger.info(f'pipeline "{self.key}" finalizado com sucesso')

        return df
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:

        cfg = self.cfg

        df.drop(columns=cfg.get('remove_columns', []), errors='ignore', inplace=True)
        df.rename(columns=cfg.get('rename_columns', {}), inplace=True)

        for col, dtype in cfg.get('column_types', {}).items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

        for col in cfg.get('datetime_columns', []):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        if 'volume' in df.columns and df['volume'].dtype == 'object':
            df['volume'] = pd.to_numeric(df['volume'].str.replace(',','.', regex=False), errors='coerce')

        if 'local_de_picking' in df.columns:
            df['local_de_picking'] = df['local_de_picking'].astype('string')
            split_cols = df['local_de_picking'].str.split('-', expand=True)

            df['rua'] = split_cols[0] if split_cols.shape[1] > 0 else pd.NA
            df['endereco'] = split_cols[1] if split_cols.shape[1] > 1 else pd.NA
            df['nivel'] = split_cols[2] if split_cols.shape[1] > 2 else pd.NA
        
        df['rua'] = df['rua'].fillna('')
        df['endereco'] = df['endereco'].fillna('')

        df['setores'] = classify_setores(df)

        df['situacao_prazo'] = check_deadline(df)

        df['localizacao'] = np.where(
            (df['rua'].isin(['CP1', 'CS1',  'P02', 'R01', 'R02'])) | (df['endereco'] == 'PAR'),
            'P.A.R',
            'Salao'
        )

        if 'data_hora_ultimo_update_olpn' in df.columns:
            df['mes_ano'] = df['data_hora_ultimo_update_olpn'].dt.strftime('%m-%Y')
            df['data_criterio'] = df['data_hora_ultimo_update_olpn'].dt.strftime('%d-%m-%Y')
            df['hora'] = df['data_hora_ultimo_update_olpn'].dt.strftime('%H:00:00')
        else:
            logger.critical('coluna "data_hora_ultimo_update_olpn" nao encontrada')

        return df
