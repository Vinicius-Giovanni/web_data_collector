# remote imports
from pathlib import Path
import pandas as pd
import numpy as np
from unidecode import unidecode

# local imports
from config.settings import PIPELINE_CONFIG
from utils.config_logger import setup_logger, log_with_context
from utils.classification import cancel_classify_setores
from utils.reader import read_csv, export_as_parquet, normalizar_motivo

# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='CancelPipeline', logger=logger)
class CancelPipeline:
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
        self.key = 'cancel'
        self.cfg = PIPELINE_CONFIG.get(self.key)

        if not self.cfg:
            logger.critical(f'pipeline {self.key} invalido')
            raise ValueError(f'pipeline {self.key} invalido')
        
    def run(self, input_path: Path, output_path: Path) -> pd.DataFrame:
        """
        run CancelPipeline
        """

        logger.info(f'Iniciando pipeline {self.key}', extra={
            'job': 'CancelPipeline',
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
                'job': 'CancelPipeline',
                'status': 'failure'
            })
            return pd.DataFrame()
        
        df = self.preprocess(df)

        if 'mes_ano' not in df.columns:
            logger.critical('coluna "mes_ano" ausente', extra={
                'job': 'CancelPipeline',
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
        df['mes_ano'] = df['data_cancelamento'].dt.strftime('%m-%Y')

        return df