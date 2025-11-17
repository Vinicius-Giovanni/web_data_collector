from pathlib import Path
import pandas as pd
import numpy as np
from config.pipeline_config import PIPELINE_CONFIG
from utils.config_logger import log_with_context
from config.pipeline_config import logger
from utils.reader import read_csv, export_as_parquet

@log_with_context(job='PendenciaASNPipeline', logger=logger)
class PendenciaASNPipeline:

    def __init__(self):
        self.key = 'pendencia_asn'
        self.cfg = PIPELINE_CONFIG.get(self.key)

        if not self.cfg:
            logger.critical(f'pipeline {self.key} nao encontrado no modulo settings.py', extra={'status': 'critico'})

    def run(self, input_path: Path, output_path: Path) -> pd.DataFrame:

        logger.info(f'Iniciando pipeline {self.key}', extra={'status':'iniciado'})

        output_path.mkdir(parents=True, exist_ok=True)

        df = read_csv(
            path=input_path,
            pipeline_key=self.key
        )

        if df.empty:
            logger.critical('dataframe vazio', extra={'status':'critico'})
            return pd.DataFrame()
        
        df = self.preprocess(df)

        export_as_parquet(df, output_folder=output_path, pipeline_key=self.key, name='1.05 - Pendencia de fechamento de ASN')

        logger.info(f'pipeline "{self.key}" finalizado com sucesso',extra={'status':'sucesso'})

        return df
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        cfg = self.cfg
        
        df.drop(columns=cfg.get('remove_columns', []),errors='ignore', inplace=True)
        df.rename(columns=cfg.get('rename_columns',{}), inplace=True)

        for col, dtype in cfg.get('column_types',{}).items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

        for col in cfg.get('datetime_columns', []):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        if 'data_integracao_wms' in df.columns:
            df['data_criterio'] = df['data_integracao_wms'].dt.strftime('%d-%m-%Y')
            df['hora'] = df['data_integracao_wms'].dt.strftime('%H:00:00')
        else:
            logger.critical('coluna "data_integracao_wms" nao encontrada no dataframe', extra={'status':'critico'})
        
        return df
        