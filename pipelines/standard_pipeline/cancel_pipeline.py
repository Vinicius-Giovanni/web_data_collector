from pathlib import Path
import pandas as pd
from unidecode import unidecode
from config.pipeline_config import PIPELINE_CONFIG
from utils.config_logger import log_with_context
from config.pipeline_config import logger
from utils.classification import cancel_classify_setores
from utils.reader import read_csv, export_as_parquet, normalizar_motivo

@log_with_context(job='CancelPipeline', logger=logger)
class CancelPipeline:

    def __init__(self):
        self.key = 'cancel'
        self.cfg = PIPELINE_CONFIG.get(self.key)

        if not self.cfg:
            logger.critical(f'pipeline {self.key} nao encontrado no modulo settings.py', extra={'status': 'critico'})
            raise ValueError(f'pipeline {self.key} nao encontrado no modulo settings.py')
        
    def run(self, input_path: Path, output_path: Path) -> pd.DataFrame:
        logger.info(f'iniciando pipeline {self.key}', extra={'status': 'iniciado'})

        input_path.mkdir(parents=True, exist_ok=True)
        output_path.mkdir(parents=True, exist_ok=True)

        df = read_csv(path=input_path, pipeline_key=self.key)

        if df.empty:
            logger.critical('dataframe vazio', extra={'status': 'critico'})
            return pd.DataFrame()
        
        df = self.preprocess(df)

        export_as_parquet(df, output_folder=output_path, pipeline_key=self.key ,name='6.10 - Pedidos Cancelados')

        logger.info(f'pipeline "{self.key}" finalizado com sucesso', extra={'status': 'sucesso'})

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

        df['setores'] = cancel_classify_setores(df)

        if 'motivo_cancelamento' in df.columns:
            df['motivo_cancelamento'] = (
                df['motivo_cancelamento']
                .fillna('')
                .str.strip()
                .replace('','sem motivo')
                .apply(lambda x: unidecode(x).lower())
            )

            result = df['motivo_cancelamento'].apply(normalizar_motivo)
            df['motivo_codigo'] = result.map(lambda x: x[0])
            df['motivo_descricao'] = result.map(lambda x: x[1])

        df['hora'] = df['data_cancelamento'].dt.strftime('%H:00:00')
        df['data_criterio'] = df['data_cancelamento'].dt.strftime('%d-%m-%Y')

        return df