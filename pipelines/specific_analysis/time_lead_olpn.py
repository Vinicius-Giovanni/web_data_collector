import pandas as pd
from config.pipeline_config import PIPELINE_CONFIG
from config.paths import PIPELINE_PATHS
from utils.config_logger import log_with_context
from config.pipeline_config import logger
from utils.reader import export_as_parquet, read_parquet_files


@log_with_context(job='TimeLeadOLPNPipeline', logger=logger)
class TimeLeadOLPNPipeline:

    def __init__(self):
        self.key = 'time_lead_olpn'
        self.cfg = PIPELINE_CONFIG.get(self.key)
        self.paths = PIPELINE_PATHS[self.key]

        if not self.cfg:
            logger.critical(
                f'pipeline "{self.key}" nao encontrado no modulo pipeline_config.py',
                extra={'status': 'critico'}
            )

    def run(self) -> pd.DataFrame:
        logger.info(f'iniciando pipeline "{self.key}"', extra={'status': 'iniciado'})

        input_path = self.paths['parquet_load']
        output_path = self.paths['output_parquet']
        output_path.mkdir(parents=True, exist_ok=True)

        df = read_parquet_files(self=self,
            folder=input_path
        )

        if df.empty:
            logger.critical('dataframe vazio — encerrando pipeline', extra={'status': 'critico'})
            return pd.DataFrame()

        df = self.preprocess(df)

        export_as_parquet(
            df,
            output_folder=output_path,
            pipeline_key=self.key,
            name='time_lead_olpn'
        )

        logger.info(f'pipeline "{self.key}" finalizado com sucesso', extra={'status': 'sucesso'})
        return df

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        cfg = self.cfg

        for col, dtype in cfg.get('column_types', {}).items():
            if col in df.columns:
                df[col] = df[col].astype(dtype)

        for col in cfg.get('datetime_columns', []):
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        if 'olpn' in df.columns:
            df = df.drop_duplicates(subset='olpn', keep='first')

        if 'data_hora_load' in df.columns:
            df = df.dropna(subset=['data_hora_load'])

        if {'data_hora_load', 'data_pedido'}.issubset(df.columns):
            df['diferenca_segundos'] = (
                (df['data_hora_load'] - df['data_pedido'])
                .dt.total_seconds()
                .abs()
                .astype('Int64')
            )
        else:
            logger.warning('colunas necessarias para calculo de diferenca nao encontradas')

        if 'data_hora_load' in df.columns:
            df['hora'] = df['data_hora_load'].dt.strftime('%H:00:00')
            df['data_criterio'] = df['data_hora_load'].dt.strftime('%d-%m-%Y')
            df['mes_ano'] = df['data_hora_load'].dt.strftime('%m-%Y')
        else:
            logger.warning('coluna "data_hora_load" ausente — hora, data_criterio e mes_ano nao serao criadas')

        logger.info('pre-processamento concluído com sucesso')
        return df
