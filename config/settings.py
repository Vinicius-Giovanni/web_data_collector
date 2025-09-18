"""
Settings Module

This module's purpose is to centralize all constants, global variables, and project configuration parameters.
It acts as a single source of thuth, ensuring that any adustments to critical values is consistently propagated throughout the application ecosystem.


Main objectives:
- Avoid duplication of definitions scattered across the codebase.
- Increase project maintainability, allowing modifications to be made in a single location.
- Provide a reliable repository of configurations for functions and classes.

Structure and responsibilities:
1. Global constants: Fixed values used across multiple modules, such as diretory names, date formats, or table schemas.
2. Execution configurations: variables controlling dynamic parameters, such as debug flags, logging levels, or processings limits.
3. Integration with functions and classes: functions and classes should import constants defined here, eliminating replication.
    Example: and ETL class can inherit folder names from the Bronze/Silver/Gold architecture directly from tis module.

Architectural benefis:
- Centralization: reduces incosistency between modules.
- Scalability: new modules can be easily integrated without redefinig existing values.
- Governance: facilitates auditing and traceabiliy of critical project parameters.

"""

from pathlib import Path
from dotenv import load_dotenv

# path for log
LOG_DIR = Path(r'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Gold (Business Layer)/logs')

# path for .env file
ENT_PATH = Path(r'C:/Users/2960006959/Desktop/project\web_data_collector/config/.env')

# path for database
DATA_BASE_PATH = Path(r'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse')

# data paths temporary for chrome
TEMP_DIR = {
    "BRONZE": {
        'olpn': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_olpn'),
        'dir_chrome_login': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_geral'),
        'cancel': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_cancel'),
        'picking': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_picking'),
        'putaway': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_putaway'),
        'packing': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_packing'),
        'loading': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_loading'),
    },
    "SILVER": {
        'olpn': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_olpn'),
        'cancel': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_cancel'),
        'picking': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_picking'),
        'putaway': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_putaway'),
        'packing': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_packing'),
        'loading': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_loading')
    },
    "GOLD": {
        'olpn': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_olpn'),
        'cancel': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_cancel'),
        'picking': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_picking'),
        'putaway': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_putaway'),
        'packing': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_packing'),
        'loading': Path(fr'{DATA_BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_loading')
    }
}