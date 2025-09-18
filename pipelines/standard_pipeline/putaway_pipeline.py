# remote imports
from pathlib import Path
import pandas as pd

# local imports
from config.settings import PIPELINE_CONFIG
from utils.config_logger import setup_logger, log_with_context
from utils.classification import classify_setores
from utils.reader import read_csv, export_as_parquet

# %(name)s <<< module name
logger = setup_logger(__name__)

@log_with_context(job='PutawayPipeline', logger=logger)
class PutawayPipeline:
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
        self.key = 'putaway'
        self.cfg = PIPELINE_CONFIG.get(self.key)

        if not self.cfg:
            logger.critical(f'pipeline {self.key} invalido')
            raise ValueError(f'pipeline {self.key} invalido')
        
    def run(self, input_path: Path, output_path: Path) -> pd.DataFrame:
        """
        run PutawayPipeline
        """
        
        logger.info(f'iniciando pipeline {self.key}', extra={
            'job': 'PutawayPipeline',
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
                'job': 'PutawayPipeline',
                'status': 'failure'
            })

            return pd.DataFrame()
        
        df = self.preprocess(df)

        if 'mes_ano' not in df.columns:
            logger.critical('coluna mes_ano nao encontrada', extra={
                'job': 'PutawayPipeline',
                'status': 'failure'
            })
            return pd.DataFrame()
        
        export_as_parquet(df, output_folder=output_path, pipeline_key=self.key, name='6.15 - Produtividade - Outbound Putaway')

        logger.info(f'pipeline {self.key} finalizado com sucesso', extra={
            'job': 'PutawayPipeline',
            'status': 'success'
        })

        return df
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        cfg = self.cfg

        df.drop(columns=cfg.get('remove_columns', []), errors='ignore', inplace=True)
        df.rename(columns=cfg.get('rename_columns',{}), inplace=True)

        for col, dtype in cfg.get('column_types', {}).items():
            if col in df.columns:
                if col == 'box':
                    df[col] = pd.to_numeric(
                        df[col].astype(str).str.extract(r'(\d+)', expand=False),
                        errors='coerce'
                    ).astype('Int64')
                else:
                    df[col] = df[col].astype(dtype)

        for col in cfg.get('datetime_columns', []):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        if 'data_hora_putaway' in df.columns:
            df['data_putaway'] = df['data_hora_putaway'].dt.date
        else:
            logger.warning('Coluna "data_hora_putaway" ausente. Cálculo de tempo será ignorado.')
        
        if {'box', 'data_putaway', 'data_hora_putaway'}.issubset(df.columns):
            time_lead_box = df.groupby(['box', 'data_putaway'])['data_hora_putaway'].agg(['min', 'max']).reset_index()
            time_lead_box['duracao_segundos_box_dia'] = (time_lead_box['max'] - time_lead_box['min']).dt.total_seconds()
            df = df.merge(time_lead_box[['box', 'data_putaway', 'duracao_segundos_box_dia']],
                          how='left', on=['box', 'data_putaway'])
        else:
            logger.warning('Dados insuficientes para calcular tempo de box por dia.')

        df['duracao_segundos_box_dia'] = df.get('duracao_segundos_box_dia', pd.Series(dtype='float')).astype('Int64')

        if 'data_hora_putaway' in df.columns:
            df['hora'] = df['data_hora_putaway'].dt.strftime('%H:00:00')
            df['data_criterio'] = df['data_hora_putaway'].dt.strftime('%d-%m-%Y')
            df['mes_ano'] = df['data_hora_putaway'].dt.strftime('%m-%Y')
        else:
            df['hora'] = df['data_criterio'] = df['mes_ano'] = 'indefinido'

        df['setores'] = classify_setores(df)

        # Limpeza final
        df.drop(columns=['key_1', 'data_putaway_x', 'data_putaway_x', 'data_putaway'], inplace=True, errors='ignore')

        logger.info(f'Pré-processamento finalizado: {df.shape[0]} linhas, {df.shape[1]} colunas.')
        return df