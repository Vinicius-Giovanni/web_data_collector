"""
reader.py Module

This module centralizes support functions for handling files and directories, integrating
with the corporate logging system through the @log_with_context decoraor.
Each implemented functions is prepared to register structured logs, enabling execution traceability,
auditing, and failure monitoring.

Architectural benefits:
- Standardization of the file handling lifecycle (creation, reading, writing, cleaning, and merging).
- Direct integration with corporate logging, ensuring and traceability across all operations.
- Reduction of complexity and code duplication across multiple modules.
- Robustness against operational failures (missing, corrupted files, or non-existent directories).
"""

import shutil
import pandas as pd
from pathlib import Path
import time
from typing import Dict
import shutil
import re
from typing import Union, Tuple
from unidecode import unidecode
from datetime import datetime, timedelta
import shutil

from utils.config_logger import setup_logger, log_with_context
from config.settings import PIPELINE_CONFIG, MOTIVOS_OFICIAIS, MAPEAMENTO_TEXTUAL, REGRAS_DIRETAS

logger = setup_logger(__name__)

@log_with_context('clear_dirs', logger)
def clear_dirs(dirs: Dict[str, any], prefix: str = '') -> None:
    """
    - Clearts the directories specified in a dictionary.
    - If they do not exist, they are created automatically.
    - Recursively removes files, symbolic links, and subdirectories with exception handlink.

    """

    for name, folder in dirs.items():
        full_name = f'{prefix}_{name}' if prefix else name
        continue

    try:
        if not folder.existis():
            