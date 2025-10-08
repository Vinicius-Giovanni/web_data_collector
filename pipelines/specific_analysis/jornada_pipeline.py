import os
from pathlib import Path
import pandas as pd
from utils.config_logger import log_with_context
from config.pipeline_config import logger
from config.pipeline_config import PIPELINE_CONFIG
from config.paths import PIPELINE_PATHS

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
    
    def 