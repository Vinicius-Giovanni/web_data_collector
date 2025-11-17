from pathlib import Path
import pandas as pd
import numpy as np
from config.pipeline_config import PIPELINE_CONFIG
from utils.config_logger import log_with_context
from config.pipeline_config import logger
from utils.classification import classify_setores, check_deadline
from utils.reader import read_csv, export_as_parquet

@Log_with_context(job='PendenciaASNPipeline', logger=logger)
class PendenciaASNPipeline:

    def __init__(self):
        self.key = 'pendencia_asn'
        self.cfg = PIPELINE_CONFIG.get(self.key)

        if not self.cfg:
            logger.critical(f'pipeline {self.key} nao encontrado no modulo settings.py', extra={'status': 'critico'})

    def run(self, input_path: Path, output_path: Path) -> pd.DataFrame:

        logger.info(f'Iniciando pipeline {self.key}', extra={'status':'iniciado'})

        output_path.mkdir(parents=True, exist_ok=True)

        