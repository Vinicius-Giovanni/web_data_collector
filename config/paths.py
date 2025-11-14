from pathlib import Path

BASE_PATH = Path(r'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse')

LOG_DIR = Path(f'{BASE_PATH}/Gold (Business Layer)/logs')
LOG_PATH = LOG_DIR / Path(r'log.log')

ENV_PATH = Path(r'C:/Users/2960006959/Desktop/web_data_collector/config/.env')

EXECUTION_MODE = Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/execution_mode.txt')

SELENIUM_CHROME = Path('C:/Users/2960006959/Desktop/selenium_chrome')

REAL_TIME_UPDATE = {
    'SELENIUM_CHROME': SELENIUM_CHROME,
    'BRONZE': {
        'olpn': Path(f'{BASE_PATH}/Features/web_data_collector/Bronze (Raw Layer)/3.11 - Status Wave + oLPN'),
        'picking': Path(f'{BASE_PATH}/Features/web_data_collector/Bronze (Raw Layer)/4.05 - Relatório de Produtividade - Picking'),
        'packing': Path(f'{BASE_PATH}/Features/web_data_collector/Bronze (Raw Layer)/5.03 - Produtividade de Packing - Packed por hora'),
        'loading': Path(f'{BASE_PATH}/Features/web_data_collector/Bronze (Raw Layer)/5.04 - Produtividade Load - Load por hora'),
        'putaway': Path(f'{BASE_PATH}/Features/web_data_collector/Bronze (Raw Layer)/6.15 - Produtividade - Outbound Putaway'),
        'expedicao': Path(f'{BASE_PATH}/Features/web_data_collector/Bronze (Raw Layer)/6.06 - Expedicao - CD')  
    },
    'SILVER': {
        'olpn': Path(f'{BASE_PATH}/Features/web_data_collector/Silver (Cleansed Layer)/3.11 - Status Wave + oLPN'),
        'picking': Path(f'{BASE_PATH}/Features/web_data_collector/Silver (Cleansed Layer)/4.05 - Relatório de Produtividade - Picking'),
        'packing': Path(f'{BASE_PATH}/Features/web_data_collector/Silver (Cleansed Layer)/5.03 - Produtividade de Packing - Packed por hora'),
        'loading': Path(f'{BASE_PATH}/Features/web_data_collector/Silver (Cleansed Layer)/5.04 - Produtividade Load - Load por hora'),
        'putaway': Path(f'{BASE_PATH}/Features/web_data_collector/Silver (Cleansed Layer)/6.15 - Produtividade - Outbound Putaway'),
        'expedicao': Path(f'{BASE_PATH}/Features/web_data_collector/Silver (Cleansed Layer)/6.06 - Expedicao - CD')   
    },
    'GOLD': {
        'olpn': Path(f'{BASE_PATH}/Features/web_data_collector/Gold (Business Layer)/3.11 - Status Wave + oLPN'),
        'picking': Path(f'{BASE_PATH}/Features/web_data_collector/Gold (Business Layer)/4.05 - Relatório de Produtividade - Picking'),
        'packing': Path(f'{BASE_PATH}/Features/web_data_collector/Gold (Business Layer)/5.03 - Produtividade de Packing - Packed por hora'),
        'loading': Path(f'{BASE_PATH}/Features/web_data_collector/Gold (Business Layer)/5.04 - Produtividade Load - Load por hora'),
        'putaway': Path(f'{BASE_PATH}/Features/web_data_collector/Gold (Business Layer)/6.15 - Produtividade - Outbound Putaway'),
        'expedicao': Path(f'{BASE_PATH}/Features/web_data_collector/Gold (Business Layer)/6.06 - Expedicao - CD')
    }
}

TEMP_DIR = {
    "BRONZE": {
        'olpn': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_olpn'),
        'dir_chrome_login': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_geral'),
        'cancel': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_cancel'),
        'picking': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_picking'),
        'putaway': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_putaway'),
        'packing': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_packing'),
        'loading': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_loading'),
        'estoque_mov': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_estoque_mov'),
        'pendencia_asn': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_pendencia_asn'),
        'recebimento': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_recebimento'),
        'expedicao': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_expedicao')
    },
    "SILVER": {
        'olpn': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_olpn'),
        'cancel': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_cancel'),
        'picking': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_picking'),
        'putaway': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_putaway'),
        'packing': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_packing'),
        'loading': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_loading'),
        'expedicao': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_expedicao')
    },
    "GOLD": {
        'olpn': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_olpn'),
        'cancel': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_cancel'),
        'picking': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_picking'),
        'putaway': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_putaway'),
        'packing': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_packing'),
        'loading': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_loading'),
        'expedicao': Path(f'{BASE_PATH}/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_expedicao')
    }
}

CLEAR_DIR = {
    'SELENIUM_CHROME': SELENIUM_CHROME,
    "BRONZE": {
        'olpn': TEMP_DIR['BRONZE']['olpn'],
        'dir_chrome_login': TEMP_DIR['BRONZE']['dir_chrome_login'],
        'cancel': TEMP_DIR['BRONZE']['cancel'],
        'picking': TEMP_DIR['BRONZE']['picking'],
        'putaway': TEMP_DIR['BRONZE']['putaway'],
        'packing': TEMP_DIR['BRONZE']['packing'],
        'loading': TEMP_DIR['BRONZE']['loading'],
        'expedicao': TEMP_DIR['BRONZE']['expedicao'],
        'pendencia_asn': TEMP_DIR['BRONZE']['pendencia_asn'],
        'recebimento': TEMP_DIR['BRONZE']['recebimento'],
        'estoque_mov': TEMP_DIR['BRONZE']['estoque_mov']
    },
    "SILVER": {
        'olpn' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '3.11 - Status Wave + oLPN'),
        'cancel' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '6.10 - Pedidos Cancelados'),
        'picking' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        'putaway' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '6.15 - Produtividade - Outbound Putaway'),
        'packing' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '5.03 - Produtividade de Packing - Packed por hora'),
        'loading' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '5.04 - Produtividade Load - Load por hora'),
        'estoque_mov' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '7.05 - Movimentacao de estoque'),
        'pendencia_asn' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '1.05 - Pendencia de fechamento de ASN'),
        'recebimento' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '1.06 - Recebimento'),
        'expedicao' : Path(BASE_PATH / 'Silver (Cleansed Layer)' / '6.06 - Expedicao - CD')
    }}
  
CLEAR_DIR_DATA_RELOAD = {
    'silver': {
        'olpn' : CLEAR_DIR['SILVER']['olpn'],
        'cancel' : CLEAR_DIR['SILVER']['cancel'],
        'picking' : CLEAR_DIR['SILVER']['picking'],
        'putaway' : CLEAR_DIR['SILVER']['putaway'],
        'packing' : CLEAR_DIR['SILVER']['packing'],
        'loading' : CLEAR_DIR['SILVER']['loading'],
        'expedicao' : CLEAR_DIR['SILVER']['expedicao']
    },
    'gold': {
        'olpn' : Path(BASE_PATH / 'Gold (Business Layer)' / '3.11 - Status Wave + oLPN'),
        'cancel' : Path(BASE_PATH / 'Gold (Business Layer)' / '6.10 - Pedidos Cancelados'),
        'picking' : Path(BASE_PATH / 'Gold (Business Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        'putaway' : Path(BASE_PATH / 'Gold (Business Layer)' / '6.15 - Produtividade - Outbound Putaway'),
        'packing' : Path(BASE_PATH / 'Gold (Business Layer)' / '5.03 - Produtividade de Packing - Packed por hora'),
        'loading' : Path(BASE_PATH / 'Gold (Business Layer)' / '5.04 - Produtividade Load - Load por hora'),
        'estoque_mov' : Path(BASE_PATH / 'Gold (Business Layer)' / '7.05 - Movimentacao de estoque'),
        'pendencia_asn' : Path(BASE_PATH / 'Gold (Business Layer)' / '1.05 - Pendencia de fechamento de ASN'),
        'recebimento' : Path(BASE_PATH / 'Gold (Business Layer)' / '1.06 - Recebimento'),
        'expedicao' : Path(BASE_PATH / 'Gold (Business Layer)' / '6.06 - Expedicao - CD')
    }
}

DATA_PATHS = {
    'bronze': {
        'olpn' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '3.11 - Status Wave + oLPN'),
        'cancel': Path(BASE_PATH / 'Bronze (Raw Layer)' / '6.10 - Pedidos Cancelados'),
        'picking' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        'putaway' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '6.15 - Produtividade - Outbound Putaway'),
        'packing' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '5.03 - Produtividade de Packing - Packed por hora'),
        'loading' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '5.04 - Produtividade Load - Load por hora'),
        'estoque_mov' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '7.05 - Movimentacao de estoque'),
        'pendencia_asn' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '1.05 - Pendencia de fechamento de ASN'),
        'recebimento' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '1.06 - Recebimento'),
        'expedicao' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '6.06 - Expedicao - CD')
    },
    'silver': {
        'olpn' : CLEAR_DIR['SILVER']['olpn'],
        'cancel' : CLEAR_DIR['SILVER']['cancel'],
        'picking' : CLEAR_DIR['SILVER']['picking'],
        'putaway' : CLEAR_DIR['SILVER']['putaway'],
        'packing' : CLEAR_DIR['SILVER']['packing'],
        'loading' : CLEAR_DIR['SILVER']['loading'],
        'estoque_mov' : CLEAR_DIR['SILVER']['estoque_mov'],
        'pendencia_asn' : CLEAR_DIR['SILVER']['pendencia_asn'],
        'recebimento' : CLEAR_DIR['SILVER']['recebimento'],
        'expedicao' : CLEAR_DIR['SILVER']['expedicao']
    },
    'gold': {
        'olpn' : CLEAR_DIR_DATA_RELOAD['gold']['olpn'],
        'cancel' : CLEAR_DIR_DATA_RELOAD['gold']['cancel'],
        'picking' : CLEAR_DIR_DATA_RELOAD['gold']['picking'],
        'putaway' : CLEAR_DIR_DATA_RELOAD['gold']['putaway'],
        'packing' : CLEAR_DIR_DATA_RELOAD['gold']['packing'],
        'estoque_mov' : CLEAR_DIR_DATA_RELOAD['gold']['estoque_mov'],
        'pendencia_asn' : CLEAR_DIR_DATA_RELOAD['gold']['pendencia_asn'],
        'recebimento' : CLEAR_DIR_DATA_RELOAD['gold']['recebimento'],
        'loading' : CLEAR_DIR_DATA_RELOAD['gold']['loading'],
        'expedicao' : CLEAR_DIR_DATA_RELOAD['gold']['expedicao'],
        'time_lead_olpn' : Path(f'{BASE_PATH}/Gold (Business Layer)/analise_time_lead_olpn'),
        'jornada' : Path(f'{BASE_PATH}/Gold (Business Layer)/jornada'),
        'bottleneck_box' : Path(f'{BASE_PATH}/Gold (Business Layer)/analise_bottleneck_box'),
        'bottleneck_salao' : Path(f'{BASE_PATH}/Gold (Business Layer)/analise_bottleneck_salao')
    }
}

FILE_ROUTER = {
    TEMP_DIR['BRONZE']['olpn'] : DATA_PATHS['bronze']['olpn'],
    TEMP_DIR['BRONZE']['cancel'] : DATA_PATHS['bronze']['cancel'],
    TEMP_DIR['BRONZE']['picking'] : DATA_PATHS['bronze']['picking'],
    TEMP_DIR['BRONZE']['putaway'] : DATA_PATHS['bronze']['putaway'],
    TEMP_DIR['BRONZE']['packing'] : DATA_PATHS['bronze']['packing'],
    TEMP_DIR['BRONZE']['loading'] : DATA_PATHS['bronze']['loading'],
    TEMP_DIR['BRONZE']['expedicao'] : DATA_PATHS['bronze']['expedicao'],
    TEMP_DIR['BRONZE']['estoque_mov'] : DATA_PATHS['bronze']['estoque_mov'],
    TEMP_DIR['BRONZE']['pendencia_asn'] : DATA_PATHS['bronze']['pendencia_asn'],
    TEMP_DIR['BRONZE']['recebimento'] : DATA_PATHS['bronze']['recebimento']
}

FILE_ROUTER_MERGE = {
    DATA_PATHS['silver']['olpn'] : DATA_PATHS['gold']['olpn'],
    DATA_PATHS['silver']['cancel'] : DATA_PATHS['gold']['cancel'],
    DATA_PATHS['silver']['picking'] : DATA_PATHS['gold']['picking'],
    DATA_PATHS['silver']['putaway'] : DATA_PATHS['gold']['putaway'],
    DATA_PATHS['silver']['packing'] : DATA_PATHS['gold']['packing'],
    DATA_PATHS['silver']['loading'] : DATA_PATHS['gold']['loading'],
    DATA_PATHS['silver']['expedicao'] : DATA_PATHS['gold']['expedicao'],
    DATA_PATHS['silver']['estoque_mov'] : DATA_PATHS['gold']['estoque_mov'],
    DATA_PATHS['silver']['pendencia_asn'] : DATA_PATHS['gold']['pendencia_asn'],
    DATA_PATHS['silver']['recebimento'] : DATA_PATHS['gold']['recebimento']
}

PIPELINE_PATHS = {
    'time_lead_olpn': {
        'parquet_load': Path(CLEAR_DIR_DATA_RELOAD['gold']['loading']),
        'output_parquet': Path(DATA_PATHS['gold']['time_lead_olpn'])
        },
    'jornada': {
        'raw': Path(f'{BASE_PATH}/Bronze (Raw Layer)/Jornada'),
        'processed': Path(f'{BASE_PATH}/Silver (Cleansed Layer)/Jornada'),
        'parquet': Path(DATA_PATHS['gold']['jornada'])
    },
    'bottleneck_salao': {
        'parquet_packed': Path(DATA_PATHS['gold']['picking']),
        'parquet_putaway': Path(DATA_PATHS['gold']['putaway']),
        'output_parquet': Path(DATA_PATHS['gold']['bottleneck_salao'])
    },
    'bottleneck_box': {
        'parquet_load': Path(DATA_PATHS['gold']['loading']),
        'parquet_putaway': Path(DATA_PATHS['gold']['putaway']),
        'output_parquet': Path(DATA_PATHS['gold']['bottleneck_box'])
    }
}