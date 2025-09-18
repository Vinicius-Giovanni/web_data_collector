# remote imports
from pathlib import Path
import pandas as pd
import numpy as np

# local imports
from config.settings import PIPELINE_CONFIG, TEMP_DIR
from utils.config_logger import setup_logger, log_with_context
from utils.classification import classify_setores
from utils.reader import read_csv, export_as_parquet, read_parquet_with_tote

# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='LoadingPipeline', logger=logger)
class LoadingPipeline:
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
        self.key = 'loading'
        self.cfg = PIPELINE_CONFIG.get(self.key)

        if not self.cfg:
            logger.critical(f'pipeline {self.key} invalido')
            raise ValueError(f'pipeline {self.key} invalido')
    
    def run(self, input_path: Path, output_path: Path) -> pd.DataFrame:
        """
        run LoadingPipeline
        """

        logger.info(f'iniciando pipeline {self.key}', extra={
            'job': 'LoadingPipeline',
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
                'job': 'LoadingPipeline',
                'status': 'failure'
            })
            return pd.DataFrame()
        
        df = self.preprocess(df)

        if 'mes_ano' not in df.columns:
            logger.critical('coluna mes_ano nao encontrada no dataframe', extra={
                'job': 'LoadingPipeline',
                'status': 'failure'
            })
            return pd.DataFrame()

        export_as_parquet(df, output_folder=output_path, pipeline_key=self.key, name='5.04 - Produtividade Load - Load por hora')

        logger.info(f'pipline {self.key} finalizado com sucesso', extra={
            'job': 'LoadingPipeline',
            'status': 'success'
            })
        
        return df


    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:

        cfg = self.cfg

        df.drop(columns=cfg.get('remove_columns',[]), errors='ignore', inplace=True)
        df.rename(columns=cfg.get('rename_columns',{}), inplace=True)

        for col, dtype in cfg.get('column_types',{}).items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

        for col in cfg.get('datetime_columns',[]):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        if 'data_hora_load' in df.columns:
            df['data_load'] = df['data_hora_load'].dt.date
        else:
            logger.warning('Coluna "data_hora_load" ausente. Cálculo de tempo será ignorado.')

        if {'box', 'data_load', 'data_hora_load'}.issubset(df.columns):
            time_lead_box = df.groupby(['box', 'data_load'])['data_hora_load'].agg(['min', 'max']).reset_index()
            time_lead_box['duracao_segundos_box_dia'] = (time_lead_box['max'] - time_lead_box['min']).dt.total_seconds()
            df = df.merge(time_lead_box[['box', 'data_load', 'duracao_segundos_box_dia']],
                          how='left', on=['box', 'data_load'])
        else:
            logger.warning('Dados insuficientes para calcular tempo de box por dia.')
        
        df['duracao_segundos_box_dia'] = df.get('duracao_segundos_box_dia', pd.Series(dtype='float')).astype('Int64')

        if 'data_hora_load' in df.columns:
            df['hora'] = df['data_hora_load'].dt.strftime('%H:00:00')
            df['data_criterio'] = df['data_hora_load'].dt.strftime('%d-%m-%Y')
            df['mes_ano'] = df['data_hora_load'].dt.strftime('%m-%Y')
        else:
            df['hora'] = df['data_criterio'] = df['mes_ano'] = 'indefinido'

        df['setores'] = classify_setores(df)

        # Limpeza final
        df.drop(columns=['key_1', 'data_load_x', 'data_load_y', 'data_load'], inplace=True, errors='ignore')

        logger.info(f'Pré-processamento finalizado: {df.shape[0]} linhas, {df.shape[1]} colunas.')
        return df  