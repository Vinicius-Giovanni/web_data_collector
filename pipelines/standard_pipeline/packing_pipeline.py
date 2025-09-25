from pathlib import Path
import pandas as pd
import numpy as np
from config.settings import PIPELINE_CONFIG, DATA_PATHS
from utils.config_logger import setup_logger, log_with_context
from utils.classification import classify_setores
from utils.reader import read_csv, export_as_parquet, read_parquet_with_tote

logger = setup_logger(__name__)

@log_with_context(job='PackingPipeline', logger=logger)
class PackingPipeline:
    def __init__(self):
        self.key = 'packing'
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
            logger.critical('dataframe vazio', extra={'status': 'critico'})
            return pd.DataFrame()
        
        df = self.preprocess(df)
        
        export_as_parquet(df, output_folder=output_path, pipeline_key=self.key, name='5.03 - Produtividade de Packing - Packed por hora')

        logger.info(f'pipeline {self.key} finalizada com sucesso', extra={'status':'sucesso'})

        return df
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        cfg = self.cfg

        olpn_ref = read_parquet_with_tote(DATA_PATHS['silver']['olpn'])

        logger.info('relatorio 3.11 - Status Wave + oLPN carregado', extra={'status': 'sucesso'})

        df.drop(columns=cfg.get('remove_columns',[]), errors='ignore', inplace=True)
        df.rename(columns=cfg.get('rename_columns',{}), inplace=True)

        for col, dtype in cfg.get('column_types',{}).items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

        for col in cfg.get('datetime_columns',[]):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                
        if 'desc_setor_item' in df.columns:
            df['desc_setor_item'] = (
                df['desc_setor_item']
                .astype('string')
                .str.replace(r'[^A-Za-zÀ-ÿ ]', '', regex=True)
                .str.strip()
            )

        if 'olpn' in df.columns and not olpn_ref.empty:
            df = df.merge(olpn_ref, on='olpn', how='left')
            logger.info("merge com relatorio 3.11 - Status Wave + oLPN realizado", extra={'status': 'sucesso'})

        if 'data_hora_packed' in df.columns:
            df['data_packed'] = df['data_hora_packed'].dt.date
        else:
            logger.warning("coluna 'data_hora_packed' nao encontrada. coluna de duracao nao sera gerada", extra={'status': 'perigoso'})

        if {'box', 'data_packed', 'data_hora_packed'}.issubset(df.columns):
            time_lead_box = df.groupby(['box', 'data_packed'])['data_hora_packed'].agg(['min', 'max']).reset_index()
            time_lead_box['duracao_segundos_box_dia'] = (time_lead_box['max'] - time_lead_box['min']).dt.total_seconds()
            df = df.merge(time_lead_box[['box', 'data_packed', 'duracao_segundos_box_dia']],
                          how='left', on=['box', 'data_packed'])
        else:
            logger.warning("coluna duracao_segundos_box_dia nao sera gerada.", extra={'status': 'perigoso'})

        if {'tote', 'data_packed', 'data_hora_packed'}.issubset(df.columns):
            time_lead_tote = df.groupby(['tote', 'data_packed'])['data_hora_packed'].agg(['min', 'max']).reset_index()
            time_lead_tote['duracao_segundos_tote_dia'] = (time_lead_tote['max'] - time_lead_tote['min']).dt.total_seconds()
            df = df.merge(time_lead_tote[['tote', 'data_packed', 'duracao_segundos_tote_dia']],
                          how='left', on=['tote', 'data_packed'])
        else:
            logger.warning("coluna de tempo box dia nao sera gerada", extra={'status': 'perigoso'})

        df['duracao_segundos_tote_dia'] = np.where(
            df['duracao_segundos_tote_dia'].notna() & (df['duracao_segundos_tote_dia'] <= 59),60,
            df['duracao_segundos_tote_dia']
        )

        df['duracao_segundos_box_dia'] = df.get('duracao_segundos_box_dia', pd.Series(dtype='float')).astype('Int64')
        df['duracao_segundos_tote_dia'] = df.get('duracao_segundos_tote_dia', pd.Series(dtype='float')).astype('Int64')

        if 'data_hora_packed' in df.columns:
            df['hora'] = df['data_hora_packed'].dt.strftime('%H:00:00')
            df['data_criterio'] = df['data_hora_packed'].dt.strftime('%d-%m-%Y')
        else:
            df['hora'] = df['data_criterio'] = df['mes_ano'] = 'indefinido'

        # Limpeza final
        df.drop(columns=['key_1', 'data_packed_x', 'data_packed_y', 'data_packed'], inplace=True, errors='ignore')

        df['setores'] = classify_setores(df)

        return df