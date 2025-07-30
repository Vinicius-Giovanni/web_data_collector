# remote imports
from pathlib import Path
from dotenv import load_dotenv
import os

# local imports
from pipelines.specific_analysis.olpn_pipeline import olpn_pipeline

# detects if it is running inside the docker container
IS_DOCKER = os.environ.get("IS_DOCKER", "0") == "1"

if IS_DOCKER:

    LOCATE = 'docker'

    # paths for linux container
    LOG_DIR = Path('/mnt/gold/logs')
    ENV_PATH = Path('/web_data_collector/config/.env')
    BASE_PATH = Path('/mnt')
    TEMP_DIR = Path('/mnt/bronze/TEMP_DIR_CHROME/web_data_collector')
    DATA_PATHS = {
        'bronze': {
            'status_olpn' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '3.11 - Status Wave + oLPN')
        },
        'silver': {
            'status_olpn' : Path(BASE_PATH / 'Silver (Business Layer)' / '3.11 - Status Wave + oLPN')
        },
        'gold': {
            'status_olpn' : Path(BASE_PATH / 'Gold (Business Layer)' / '3.11 - Status Wave + oLPN')
        }
    }

else:

    LOCATE = 'windows'
    
    # --- paths for windows container ---

    # path for logs
    LOG_DIR = Path(r'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Gold (Business Layer)/logs')

    # path for .env file
    ENV_PATH = Path(r'C:/Users/2960006959/Desktop/project\web_data_collector/config/.env')

    # path for base data
    BASE_PATH = Path(r'C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse')
    
    # data paths temporary for chrome
    TEMP_DIR = {
        "DIR_CHROME": Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector')
}
    # all data paths
    DATA_PATHS = {
        'bronze': {
            'olpn' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '3.11 - Status Wave + oLPN')
        },
        'silver': {
            'olpn' : Path(BASE_PATH / 'Silver (Business Layer)' / '3.11 - Status Wave + oLPN')
        },
        'gold': {
            'olpn' : Path(BASE_PATH / 'Gold (Business Layer)' / '3.11 - Status Wave + oLPN')
        }
    }

LOG_PATH = LOG_DIR / Path(r'log_web_data_collector.log')

load_dotenv(dotenv_path=ENV_PATH)

EMAIL = os.getenv('LOGIN_EMAIL')
PASSWORD = os.getenv('LOGIN_PASSWORD')

ELEMENTS = {
    'frame': '//*[@id="rsIFrameManager_1"]',
    'ELEMENTS_LOGIN': {
        'namespace_dropdown_button': 'downshift-0-toggle-button',
        'namespace_azuread': 'downshift-0-item-0',
        'email': 'i0116',
        'password': 'i0118',
        'submit_button': 'idSIButton9',
        'element_title': 'ibm',
        'element_banner': 'bannerLogo',
        'element_title_v2': 'bx--row',
    },
    'ELEMENTS_OLPN': {
        'element_filial_id': 'dv17_ValueComboBox',
        'element_filial': '1200',
        'element_title': 'tt',
        'element_dt_start': 'dv58__tblDateTextBox__txtInput',
        'element_dt_end': 'dv66__tblDateTextBox__txtInput',
        'element_listbox': '//*[@id="dv74_MultiSelectList"]',
        'elements_listbox': '//tr[@role="option" and @checkboxitem="true"]',
        'element_get_item': 'aria-label',
        'element_get_checked': 'aria-checked',
        'element_confirm': 'dv134',
        'list_itens': [
            'S01 - ENTREGA A CLIENTES',
            'S02 - RETIRA CLIENTE DEPOSITO',
            'S03 - TRANSF.LOJA/ENTREGA CLIENTE',
            'S04 - TRANSF EAD AUTOMATICA',
            'S05 - TRANSF EAD PROGRAMADA',
            'S06- ENTREGA A CLIENTE REMANEJADA',
            'S07 - EAD AUTOMATICO REMANEJADA',
            'S08 - TRANSF.LOJA/ENTR. CLIENTE REM',
            'S09 - TRANSF. PROGRAMADA REMANEJADA',
            'S10 - REM.FORNECEDOR ASSIST.TECNICA',
            'S11 - TRANSF. LOJA VIA DEPOSITO BOA',
            'S12 - TRANSF.LOJA VIA DEPOSITO QEB',
            'S13 - ABASTECIMENTO DE LOJA BOA',
            'S14 - ABASTECIMENTO DE LOJA QEB',
            'S15 - OUTRAS SAIDAS BOA',
            'S16 - OUTRAS SAIDAS QEB',
            'S18 - REMESSA PARA CONSERTO',
            'S19 - DEVOLUÇÃO P/ FORNECEDOR A1',
            'S26 - EXPEDIÇÃO DE EAD AUTOMATICO',
            'S27 - REMESSA PARA DEPOSITO QEB',
            'S28 - REMANEJADO EAD AUTOMATICO',
            'S29 - ABM CROSS DOCK BOA',
            'S30 - ABM CROSS DOCK QEB',
            'S31 - EXP PED RET 31',
            'S32 - EAD VVLOG',
            'S33 - VENDA MIUDEZAS',
            'S34 - DEV EAD BOM',
            'S35 - DEV EAD RETIRA CLIENTE',
            'S39 - EXPEDICAO LEVES',
            'S39I - EXPEDICAO LEVES',
            'S39M - EXPEDICAO LEVES',
            'S39P - EXPEDICAO LEVES',
            'S39R - Single line',
            'S41 - INTERCOMPANY BOA',
            'S42 - INTERCOMPANY QEB',
            'S43 - ENTREGA BARATEIRO',
            'S44 - ENTREGA BARATEIRO LEVES',
            'S45 - EXPEDIÇÃO ENTREGA PELOEXTRA',
            'S46 - ABASTECIMENTO RETIRA LOJA',
            'S48 - ABASTECIMENTO CEL RJ',
            'S53 - TRANSFERENCIA ENTRE CDS',
            'S55 - EAD Faturado (Pesado)',
            'S56 - EAD Faturado (Leves)',
            'S56I - EAD Faturado (Leves)',
            'S56M - EAD Faturado (Leves)',
            'S56P - EAD Faturado (Leves)',
            'S56R - Transit point singleline',
            'S71 - SAIDAS QE FILIAL VIRTUAL 0014',
            'S99 - Intercompany'
        ]
    }
}

LINKS = {
    'LOGIN_CSI': 'https://viavp-sci.sce.manh.com/bi/?perspective=home',
    'LOGIN_OLPN' : 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=i79E326D8D72B45F795E0897FCE0606F6&objRef=i79E326D8D72B45F795E0897FCE0606F6&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22i79E326D8D72B45F795E0897FCE0606F6%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%223.11%20-%20Status%20Wave%20%2B%20oLPN%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D'
}

FILE_ROUTER = {
    '3.11 - Status Wave + oLPN': olpn_pipeline,
    '4.05 - Relatório de Produtividade - Picking': 'picking_pipeline',
    '5.03 - Produtividade de Packing - Packed por hora': 'packing_pipeline',
    '5.04 - Produtividade Load - Load por hora': 'load_pipeline',
    '6.10 - Pedidos Cancelados': 'cancelados_pipeline',
    '6.15 - Produtividade - Outbound Putaway': 'putaway_pipeline'
}