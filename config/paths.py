from pathlib import Path

# path for base data
BASE_PATH = Path(r'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse')

# path for logs
LOG_DIR = Path(f'{BASE_PATH}/Gold (Business Layer)/logs')
LOG_PATH = LOG_DIR / Path(r'log.log')

# path for .env file
ENV_PATH = Path(r'C:/Users/2960006959/Desktop/project\web_data_collector/config/.env')

EXECUTION_MODE = Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/execution_mode.txt')

# data paths temporary for chrome
TEMP_DIR = {
    "BRONZE": {
        'olpn': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_olpn'),
        'dir_chrome_login': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_geral'),
        'cancel': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_cancel'),
        'picking': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_picking'),
        'putaway': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_putaway'),
        'packing': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_packing'),
        'loading': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_loading'),
    },
    "SILVER": {
        'olpn': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_olpn'),
        'cancel': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_cancel'),
        'picking': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_picking'),
        'putaway': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_putaway'),
        'packing': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_packing'),
        'loading': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_loading')
    },
    "GOLD": {
        'olpn': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_olpn'),
        'cancel': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_cancel'),
        'picking': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_picking'),
        'putaway': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_putaway'),
        'packing': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_packing'),
        'loading': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_loading')
    }
}

CLEAR_DIR = {
    "BRONZE": {
        'olpn': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_olpn'),
        'dir_chrome_login': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_geral'),
        'cancel': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_cancel'),
        'picking': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_picking'),
        'putaway': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_putaway'),
        'packing': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_packing'),
        'loading': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_loading'),
    },
    "SILVER": {
        'olpn' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '3.11 - Status Wave + oLPN'),
        'cancel' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '6.10 - Pedidos Cancelados'),
        'picking' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        'putaway' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '6.15 - Produtividade - Outbound Putaway'),
        'packing' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '5.03 - Produtividade de Packing - Packed por hora'),
        'loading' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '5.04 - Produtividade Load - Load por hora'),
    }}

    
CLEAR_DIR_DATA_RELOAD = {
    'silver': {
        'olpn' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '3.11 - Status Wave + oLPN'),
        'cancel' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '6.10 - Pedidos Cancelados'),
        'picking' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        'putaway' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '6.15 - Produtividade - Outbound Putaway'),
        'packing' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '5.03 - Produtividade de Packing - Packed por hora'),
        'loading' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '5.04 - Produtividade Load - Load por hora'),
    },
    'gold': {
        'olpn' : Path(BASE_PATH / 'Gold (Business Layer)' / '3.11 - Status Wave + oLPN'),
        'cancel' : Path(BASE_PATH / 'Gold (Business Layer)' / '6.10 - Pedidos Cancelados'),
        'picking' : Path(BASE_PATH / 'Gold (Business Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        'putaway' : Path(BASE_PATH / 'Gold (Business Layer)' / '6.15 - Produtividade - Outbound Putaway'),
        'packing' : Path(BASE_PATH / 'Gold (Business Layer)' / '5.03 - Produtividade de Packing - Packed por hora'),
        'loading' : Path(BASE_PATH / 'Gold (Business Layer)' / '5.04 - Produtividade Load - Load por hora')
    }
}

# all data paths
DATA_PATHS = {
    'bronze': {
        'olpn' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '3.11 - Status Wave + oLPN'),
        'cancel': Path(BASE_PATH / 'Bronze (Raw Layer)' / '6.10 - Pedidos Cancelados'),
        'picking' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        'putaway' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '6.15 - Produtividade - Outbound Putaway'),
        'packing' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '5.03 - Produtividade de Packing - Packed por hora'),
        'loading' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '5.04 - Produtividade Load - Load por hora')
    },
    'silver': {
        'olpn' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '3.11 - Status Wave + oLPN'),
        'cancel' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '6.10 - Pedidos Cancelados'),
        'picking' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        'putaway' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '6.15 - Produtividade - Outbound Putaway'),
        'packing' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '5.03 - Produtividade de Packing - Packed por hora'),
        'loading' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '5.04 - Produtividade Load - Load por hora'),
    },
    'gold': {
        'olpn' : Path(BASE_PATH / 'Gold (Business Layer)' / '3.11 - Status Wave + oLPN'),
        'cancel' : Path(BASE_PATH / 'Gold (Business Layer)' / '6.10 - Pedidos Cancelados'),
        'picking' : Path(BASE_PATH / 'Gold (Business Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        'putaway' : Path(BASE_PATH / 'Gold (Business Layer)' / '6.15 - Produtividade - Outbound Putaway'),
        'packing' : Path(BASE_PATH / 'Gold (Business Layer)' / '5.03 - Produtividade de Packing - Packed por hora'),
        'loading' : Path(BASE_PATH / 'Gold (Business Layer)' / '5.04 - Produtividade Load - Load por hora')
    }
}

# function move_files
FILE_ROUTER = {
    TEMP_DIR['BRONZE']['olpn'] : DATA_PATHS['bronze']['olpn'],
    TEMP_DIR['BRONZE']['cancel'] : DATA_PATHS['bronze']['cancel'],
    TEMP_DIR['BRONZE']['picking'] : DATA_PATHS['bronze']['picking'],
    TEMP_DIR['BRONZE']['putaway'] : DATA_PATHS['bronze']['putaway'],
    TEMP_DIR['BRONZE']['packing'] : DATA_PATHS['bronze']['packing'],
    TEMP_DIR['BRONZE']['loading'] : DATA_PATHS['bronze']['loading']
}

# function merge_files
FILE_ROUTER_MERGE = {
    DATA_PATHS['silver']['olpn'] : DATA_PATHS['gold']['olpn'],
    DATA_PATHS['silver']['cancel'] : DATA_PATHS['gold']['cancel'],
    DATA_PATHS['silver']['picking'] : DATA_PATHS['gold']['picking'],
    DATA_PATHS['silver']['putaway'] : DATA_PATHS['gold']['putaway'],
    DATA_PATHS['silver']['packing'] : DATA_PATHS['gold']['packing'],
    DATA_PATHS['silver']['loading'] : DATA_PATHS['gold']['loading']
}