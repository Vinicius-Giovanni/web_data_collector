import os
from pathlib import Path
import pandas as pd
from utils.config_logger import log_with_context
from config.pipeline_config import logger
from config.pipeline_config import PIPELINE_CONFIG
from config.paths import PIPELINE_PATHS
from utils.reader import read_csv, export_as_parquet

@log_with_context(job='JornadaPipeline', logger=logger)
class JornadaPipeline:

    def __init__(self):
        self.key = 'jornada'
        self.cfg = PIPELINE_CONFIG[self.key]
        self.paths = PIPELINE_PATHS[self.key]

        if not self.cfg:
            logger.critical(
                f'pipeline "{self.key}" nao encontrado no modulo pipeline_config.py',
                extra={'status':'critico'}
            )
    
    def run(self) -> pd.DataFrame:

        logger.critical(f'iniciando pipeline "{self.key}"', extra={'status':'critico'})

        input_path = self.paths['raw']
        parquet_path = self.path = self.paths['parquet']

        input_path.mkdir(parents=True, exist_ok=True)
        parquet_path.mkdir(parents=True, exist_ok=True)

        df = read_csv(
            path=input_path,
            pipeline_key=self.key
        )

        if df.empty:
            logger.critical('dataframe vazio', extra={'status':'critico'})
            return pd.DataFrame()
        
        df = self.preprocess(df)

        export_as_parquet(
            df,
            output_folder=parquet_path,
            pipeline_key=self.key,
            name='jornada'
        )

        logger.info(f'pipeline "{self.key}" finalizado com sucesso', extra={'status':'sucesso'})
        return df
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:

        df.drop(columns=self.cfg.get('remove_columns', []), errors='ignore', inplace=True)
        df.rename(columns=self.cfg.get('rename_columns', {}), inplace=True)

        for col, dtype in self.cfg.get('column_types', {}).items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)
        
        for col in self.cfg.get('datetime_columns', []):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')

        if 'hora' in df.columns:
            df = df.loc[df['hora'].notna() & (df['hora'] != '')].copy()
            df['hora'] = pd.to_datetime(df['hora'], format='%H:%M', errors='coerce').dt.strftime('%H:%M')
            df['jornada_segundos'] = pd.to_timedelta(df['hora'] + ':00').dt.total_seconds().astype('Int64')

        df['matricula_formatada'] = df['matricula'].apply(
            lambda x: str(int(float(x))) if pd.notna(x) else '00000000'
        ).str.zfill(8)

        df['matricula_formatada'] = df['matricula'].astype('Int64').astype(str).str.zfill(8)
        df['cod'] = pd.to_numeric(df['cod'], errors='coerce').fillna(0).astype('Int64').astype(str)
        df['login'] = df['cod'] + df['matricula_formatada'] + '@viavarejo.com.br'
        df['data_criterio'] = df['data'].dt.strftime('%d-%m-%Y')
        
        required_cols = ['data','hora','jornada_segundos','login']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            return pd.DataFrame()
        
        return df