from pathlib import Path
import pandas as pd
import numpy as np
from config.settings import PIPELINE_CONFIG
from utils.config_logger import setup_logger, log_with_context
from utils.classification import classify_setores_picking
from utils.reader import read_csv, export_as_parquet

logger = setup_logger(__name__)

@log_with_context(job='PickingPipeline', logger=logger)
class PickingPipeline:
    def __init__(self):
        self.key = 'picking'
        self.cfg = PIPELINE_CONFIG.get(self.key)

        if not self.cfg:
            logger.critical(f'pipeline {self.key} nao encontrado no modulo settings.py', extra={'status': 'critico'})
            raise ValueError(f'pipeline {self.key} nao encontrado no modulo settings.py')
        
    def run(self, input_path: Path, output_path: Path) -> pd.DataFrame:
        logger.info(f'iniciando pipeline {self.key}', extra={'status': 'iniciado'})

        input_path.mkdir(parents=True, exist_ok=True)
        output_path.mkdir(parents=True, exist_ok=True)

        df = read_csv(
            path=input_path,
            pipeline_key=self.key
        )

        if df.empty:
            logger.critical('nenhum dado no dataframe', extra={'status': 'critico'})
            return pd.DataFrame()
        
        df = self.preprocess(df)
        
        export_as_parquet(df, output_folder=output_path, pipeline_key=self.key, name='4.05 - Relatório de Produtividade - Picking')

        logger.info(f'pipeline {self.key} finalizado com sucesso', extra={'status': 'sucesso'})

        return df
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        cfg = self.cfg

        df.drop(columns=cfg.get('remove_columns', []), errors='ignore', inplace=True)
        df.rename(columns=cfg.get('rename_columns',{}), inplace=True)

        for col, dtype in cfg.get('column_types', {}).items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)
        
        for col in cfg.get('datetime_columns', []):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        df['duracao_tarefa_segundos'] = (
            df['data_hora_fim_tarefa'] - df['data_hora_inicio_tarefa']
        ).dt.total_seconds().abs().astype('Int64')

        df['duracao_olpn_segundos'] = (
            df['data_hora_fim_olpn'] - df['data_hora_inicio_tarefa']
        ).dt.total_seconds().abs().astype('Int64')

        if 'local_de_picking' in df.columns:
            df['local_de_picking'] = df['local_de_picking'].astype('string')
            split_cols = df['local_de_picking'].str.split('-', expand=True)

            df['rua'] = split_cols[0] if split_cols.shape[1] > 0 else pd.NA
            df['endereco'] = split_cols[1] if split_cols.shape[1] > 1 else pd.NA
            df['nivel'] = split_cols[2] if split_cols.shape[1] > 2 else pd.NA

        df['rua'] = df['rua'].fillna('')
        df['endereco'] = df['endereco'].fillna('')

        df['localizacao'] = np.where(
            (df['rua'].isin(['CP1', 'CS1', 'P02', 'R01', 'R02'])) | (df['endereco'] == 'PAR'),
            'P.A.R',
            'Salao'
        )

        df['setores'] = classify_setores_picking(df)

        if 'data_hora_fim_olpn' in df.columns:
            df['data_criterio'] = df['data_hora_fim_olpn'].dt.strftime('%d-%m-%Y')
            df['hora'] = df['data_hora_fim_olpn'].dt.strftime('%H:00:00')
        else:
            logger.warning('coluna "data_hora_fim_olpn" ausente, data_criterio e hora nao serao criados', extra={'status': 'perigoso'})
        
        return df