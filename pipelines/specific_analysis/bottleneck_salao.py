import pandas as pd
from config.pipeline_config import PIPELINE_CONFIG
from config.paths import PIPELINE_PATHS
from utils.config_logger import log_with_context
from config.pipeline_config import logger
from utils.reader import export_as_parquet, read_parquet_folder_columns

@log_with_context(job='BottleneckSalaoPipeline', logger=logger)
class BottleneckSalaoPipeline:

    def __init__(self):
        self.key = 'bottleneck_salao'
        self.cfg = PIPELINE_CONFIG[self.key]
        self.paths = PIPELINE_PATHS[self.key]

        if not self.cfg:
            logger.critical(
                f'pipeline "{self.key}" nao encontrado no modulo pipeline_config.py',
                extra={'status':'critico'}
            )

    def run(self) -> pd.DataFrame:
        logger.info(f'iniciando pipeline "{self.key}"', extra={'status':'iniciado'})

        output_path = self.paths['output_parquet']
        output_path.mkdir(parents=True, exist_ok=True)

        df_packed = read_parquet_folder_columns(
            self=self,
            folder_path=self.paths['parquet_packed'],
            columns=self.cfg['read_columns_packed'])
        
        df_putaway = read_parquet_folder_columns(
            self=self,
            folder_path=self.paths['parquet_putaway'],
            columns=self.cfg['read_columns_putaway'])
        
        if df_packed.empty or df_putaway.empty:
            logger.critical('dataframes vazios - encerrando pipeline', extra={'status':'critico'})
            return pd.DataFrame()
        
        df_packed['olpn'] = df_packed['olpn'].astype(self.cfg['column_type']['olpn'])
        df_putaway['olpn'] = df_putaway['olpn'].astype(self.cfg['column_type']['olpn'])

        df = pd.merge(df_packed, df_putaway, on='olpn', how='left')
        df = df.drop_duplicates(subset='olpn', keep='first')
        df = df.dropna(subset=['data_hora_putaway'])

        df = self.preprocess(df)

        export_as_parquet(
            df,
            output_folder=output_path,
            pipeline_key=self.key,
            name='bottleneck_box'
        )

        logger.info(f'pipeline "{self.key}" finalizado com sucesso', extra={'status': 'sucesso'})
        return df

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:

        for col in self.cfg['datetime_columns']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        df['diferenca_segundos'] = (
            (df['data_hora_putaway'] - df['data_hora_fim_olpn'])
            .dt.total_seconds().abs()
        ).astype('Int64')

        df['data_criterio'] = df['data_hora_putaway'].dt.strftime('%d-%m-%Y')

        output_path = self.paths['output_parquet']
        output_path.mkdir(parents=True, exist_ok=True)

        return df