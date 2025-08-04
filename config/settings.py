# remote imports
from pathlib import Path
from dotenv import load_dotenv
import os

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
    
    TEMP_DIR_BASE = {
        "DIR_CHROME_BASE": Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector'),
}   
    # data paths temporary for chrome
    TEMP_DIR = {
        "BRONZE": {
            'olpn': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_olpn'),
            'dir_chrome_login': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_geral'),
            'cancel': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_cancel'),
            'picking': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/raw_temp/raw_temp_picking'),
        },
        "SILVER": {
            'olpn': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_olpn'),
            'cancel': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/silver_temp/silver_temp_cancel'),
            'picking': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/silver_temp_picking')
        },
        "GOLD": {
            'olpn': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_olpn'),
            'cancel': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_cancel'),
            'picking': Path('C:/Users/2960006959/OneDrive - Grupo Casas Bahia S.A/Sala PCP - Online_A.B.S - Data Lakehouse/Bronze (Raw Layer)/TEMP_DIR_CHROME/web_data_collector/gold_temp/gold_temp_picking')
        }
    }


    # all data paths
    DATA_PATHS = {
        'bronze': {
            'olpn' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '3.11 - Status Wave + oLPN'),
            'cancel': Path(BASE_PATH / 'Bronze (Raw Layer)' / '6.10 - Pedidos Cancelados'),
            'picking' : Path(BASE_PATH / 'Bronze (Raw Layer)' / '4.05 - Relatório de Produtividade - Picking')
        },
        'silver': {
            'olpn' : Path(BASE_PATH / 'Silver (Business Layer)' / '3.11 - Status Wave + oLPN'),
            'cancel' : Path(BASE_PATH / 'Silver (Business Layer)' / '6.10 - Pedidos Cancelados'),
            'picking' : Path(BASE_PATH / 'Silver (Business Layer)' / '4.05 - Relatório de Produtividade - Picking'),
        },
        'gold': {
            'olpn' : Path(BASE_PATH / 'Gold (Business Layer)' / '3.11 - Status Wave + oLPN'),
            'cancel' : Path(BASE_PATH / 'Gold (Business Layer)' / '6.10 - Pedidos Cancelados'),
            'picking' : Path(BASE_PATH / 'Gold (Business Layer)' / '4.05 - Relatório de Produtividade - Picking')
        }
    }

LOG_PATH = LOG_DIR / Path(r'log_web_data_collector.log')

load_dotenv(dotenv_path=ENV_PATH)

EMAIL = os.getenv('LOGIN_EMAIL')
PASSWORD = os.getenv('LOGIN_PASSWORD')

CHUNKSIZE = 200_000

FILE_ROUTER = {
    '3.11 - Status Wave + oLPN': TEMP_DIR['SILVER']['olpn'],
    '4.05 - Relatório de Produtividade - Picking': TEMP_DIR['SILVER']['picking'],
    '5.03 - Produtividade de Packing - Packed por hora': '',
    '5.04 - Produtividade Load - Load por hora': '',
    '6.10 - Pedidos Cancelados': TEMP_DIR['SILVER']['cancel'],
    '6.15 - Produtividade - Outbound Putaway': ''
}

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
    },
    'ELEMENTS_CANCEL': {
        'element_filial_id': 'dv20_ValueComboBox',
        'element_filial': '1200',
        'element_dt_start': 'dv62__tblDateTextBox__txtInput',
        'element_dt_end': 'dv71__tblDateTextBox__txtInput',
        'element_confirm': 'dv81'
    },
    'ELEMENTS_PICKING': {
        'element_filial_id': 'dv18_ValueComboBox',
        'element_filial': '1200',
        'element_dt_start': 'dv113__tblDateTextBox__txtInput',
        'element_dt_end': 'dv123__tblDateTextBox__txtInput',
        'element_listbox': '//*[@id="dv57_MultiSelectList"]',
        'elements_listbox': '//tr[@role="option" and @checkboxitem="true"]',
        'element_get_item': 'aria-label',
        'element_get_checked': 'aria-checked',
        'element_confirm': 'dv138',
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
    'LOGIN_OLPN' : 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=i79E326D8D72B45F795E0897FCE0606F6&objRef=i79E326D8D72B45F795E0897FCE0606F6&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22i79E326D8D72B45F795E0897FCE0606F6%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%223.11%20-%20Status%20Wave%20%2B%20oLPN%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D',
    'LOGIN_CANCEL': 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=iD732BE4B1DA6487F8ACD69248DA2CC19&objRef=iD732BE4B1DA6487F8ACD69248DA2CC19&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22iD732BE4B1DA6487F8ACD69248DA2CC19%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%226.10%20-%20Pedidos%20Cancelados%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D',
    'LOGIN_PICKING': 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=iC20581CB9B43482BB800469299636529&objRef=iC20581CB9B43482BB800469299636529&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22iC20581CB9B43482BB800469299636529%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%224.05%20-%20Relat%C3%B3rio%20de%20Produtividade%20-%20Picking%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D'
}

PIPELINE_CONFIG = {
        'bottleneck_salao': {
        'read_columns_packed': [
            'olpn',
            'data_hora_fim_olpn'
        ],
        'read_columns_putaway': [
            'olpn',
            'data_hora_putaway'
        ],
        'datetime_columns': [
            'data_hora_fim_olpn',
            'data_hora_putaway'
        ],
        'column_type': {
            'olpn': 'string'
        }
    },
        'bottleneck_box': {
        'read_columns_load': [
                'olpn',
                'data_hora_load'
                ],
        'read_columns_putaway': [
                'olpn',
                'data_hora_putaway'
                ],
        'datetime_columns': [
            'data_hora_putaway',
            'data_hora_load'
        ],
        'column_type': {
            'olpn': 'string'
        }

    },
        'time_lead_olpn': {
        'read_columns': [
            'olpn',
            'data_hora_load',
            'data_pedido'
        ],
        'datetime_columns': [
            'data_hora_load',
            'data_pedido'
        ],
        'column_types': {
            'olpn': 'string'
        },
    },
        'olpn': {
        'remove_columns': [
                'Cod Setor Item',
                'Inventory Type ID',
                'Data Limite Expedição',
                'Data Prevista Entrega',
                'Marcação de EAD',
                'Numero da Gaiola',
                'Tarefa Status',
                'Data do Pedido',
                'Filial',
                'Shipment',
                'Filial Destino',
                'Status Pedido',
                'Pedido de Venda',
                'Wave',
                'Descrição'
        ],
        'rename_columns': {
                'Status oLPN': 'status_olpn',
                'Data locação pedido': 'data_locacao_pedido',   
                'Audit Status': 'audit_status',
                'Último Update oLPN': 'data_hora_ultimo_update_olpn',
                'TOTE': 'tote',
                'Tarefa': 'tarefa',
                'Grupo de Tarefa': 'grupo_de_tarefa',
                'Item': 'item',
                'Local de Picking': 'local_de_picking',
                'Qtde. Peças Item': 'qt_pecas',
                'Volume': 'volume',
                'BOX': 'box',
                'Desc Setor Item': 'desc_setor_item',
                'Tipo de pedido': 'tipo_de_pedido',
                'Pedido': 'pedido',
                'oLPN': 'olpn'
        },
        'column_types': {
                'status_olpn': 'string',
                'audit_status': 'string',
                'tote': 'string',
                'tarefa': 'string',
                'grupo_de_tarefa': 'string',
                'item': 'Int64',
                'descricao': 'string',
                'local_de_picking': 'string',
                'qt_pecas': 'Int64',
                'box': 'Int64',
                'desc_setor_item': 'string',
                'tipo_de_pedido': 'string',
                'pedido': 'string',
                'olpn': 'string'
        },
        'datetime_columns':  [
                'data_locacao_pedido',
                'data_hora_ultimo_update_olpn'
        ],
        'encoding': 'utf-16',
        'sep' : '\t'
    },
        'picking': {
        'remove_columns': [
                'Filial',
                'Status Tarefa',
                'Tipo de Transação',
                'Qtde Alocada',
                'Task Moviment',
                'Pull Location for Task Detail',
                'Destination Location for Task Detail',
                'Wave',
                'Nome',
                'Data da Tarefa (Create)',
                'Data e Hora da Assinatura da Tarefa',
                'Descrição',
                'Local Destino',
                'Inventory Type',
                'Status Detalhe da Tarefa'
        ],
        'rename_columns': {
                'Tarefa': 'tarefa',
                'Qtde requerida': 'qt_requerida',
                'Qtde Separada': 'qt_separada',
                'Usuário': 'usuario',
                'Data do Inicio da Tarefa': 'data_hora_inicio_tarefa',
                'Data de Finalização da Tarefa': 'data_hora_fim_tarefa',
                'Data de Finalização da oLPN': 'data_hora_fim_olpn',
                'Order ID': 'pedido',
                'oLPN': 'olpn',
                'Item': 'item',
                'Setor': 'desc_setor_item',
                'Tipo de Pedido': 'tipo_de_pedido',
                'Local de Coleta': 'local_de_picking',
                'BOX': 'box'
        },
        'column_types': {
                'tarefa': 'string',
                'qt_requerida': 'Int64',
                'qt_separada': 'Int64',
                'usuario': 'string',
                'pedido': 'Int64',
                'olpn': 'string',
                'item': 'Int64',
                'desc_setor_item': 'string',
                'tipo_de_pedido': 'string',
                'local_de_picking': 'string',
                'box': 'Int64'
                        },
        'datetime_columns':  [
                'data_hora_inicio_tarefa',
                'data_hora_fim_tarefa',
                'data_hora_fim_olpn'
        ],
        'encoding': 'utf-16',
        'sep' : '\t'
    },
        'cancel' : {
        'remove_columns': [
                'Filial',
                'Inventory Type ID',
                'Pedido de Venda',
                'Carga',
                'Destinatário',
                'Descrição do item',
                'Qtde Original',
                'Qtde Expedida',
                'Data integração WMS',
                'Código Reference Text'
        ],
        'rename_columns': {
                'Pedido': 'pedido',
                'Tipo da Ordem ': 'tipo_de_pedido',
                'Qtde Ajustada': 'qt_pecas',
                'Data do Cancelamento': 'data_cancelamento',
                'Usuário': 'usuario',
                ' Motivo Secondary Reference Text': 'motivo_cancelamento'
        },
        'column_types': {
                'pedido': 'string',
                'tipo_de_pedido': 'string',
                'qt_pecas': 'Int64',
                'usuario': 'string',
                'motivo_cancelamento': 'string',
                'item': 'Int64'
        },
        'datetime_columns': [
                'data_cancelamento'
        ],
        'encoding': 'utf-16',
        'sep': '\t'
    },
        'packing' : {
        'remove_columns': [
                'Filial',
                'Inventory Type ID',
                'Pallet',
                'Descrição item',
                'Data Pedido',
                'Nome do Usuário',
                'Shipment',
                'Pedido venda',
                'Nota Fiscal',
                'Embala',
                'Facility ID',
                'Tipo de Pedido',
                'Data LOAD',
                'Pedido de Venda',
                'Descrição do Item'
        ],
        'rename_columns': {
                'OLPN': 'olpn',
                'Pedido': 'pedido',
                'Item': 'item',
                'Setor': 'desc_setor_item',
                'Tipo Pedido': 'tipo_de_pedido',
                'Data Packed': 'data_hora_packed',
                'Usuário': 'usuario',
                'Quantidade': 'qt_pecas',
                'BOX': 'box'
        },
        'column_types': {
                'olpn': 'string',
                'pedido': 'string',
                'item': 'Int64',
                'desc_setor_item': 'string',
                'tipo_de_pedido': 'string',
                'usuario': 'string',
                'qt_pecas': 'Int64',
                'box': 'Int64'
        },
        'datetime_columns': [
                'data_hora_packed'
        ],
        'encoding': 'utf-16',
        'sep': '\t'
    },
        'load' : {
        'remove_columns': [
                'Facility ID',
                'Inventory Type ID',
                'Nome do Usuário',
                'Shipment',
                'Pedido de Venda',
                'Nota Fiscal',
                'Descrição do Item'
        ],
        'rename_columns': {
                'OLPN': 'olpn',
                'Pedido': 'pedido',
                'Tipo de Pedido': 'tipo_de_pedido',
                'Data LOAD': 'data_hora_load',
                'Usuário': 'usuario',
                'Quantidade': 'qt_pecas',
                'BOX': 'box',
                'Item': 'item',
                'Data Pedido': 'data_pedido'
        },
        'column_types': {
                'olpn': 'string',
                'pedido': 'string',
                'tipo_de_pedido': 'string',
                'usuario': 'string',
                'qt_pecas': 'Int64',
                'box': 'Int64',
                'Item': 'Int64'
        },
        'datetime_columns': [
                'data_hora_load',
                'data_pedido'
        ],
        'encoding': 'utf-16',
        'sep': '\t'
    },
        'putaway' : {
        'remove_columns': [
                'Filial',
                'Data',
                'Status',
                'DESCRIÇÃO ITEM',
                'Item Attribute1',
                'Transaction Type',
                'Inventory Type ID'
        ],
        'rename_columns': {
                'Order': 'pedido',
                'OLPN': 'olpn',
                'ITEM': 'item',
                'QT': 'qt_pecas',
                'Setor': 'desc_setor_item',
                'Tipo de Pedido': 'tipo_de_pedido',
                'BOX': 'box',
                'DATA DO EVENTO': 'data_hora_putaway',
                'USUÁRIO': 'usuario'
        },
        'column_types': {
                'pedido': 'string',
                'olpn': 'string',
                'item': 'Int64',
                'qt_pecas': 'Int64',
                'desc_setor_item': 'string',
                'tipo_de_pedido': 'string',
                'box': 'Int64',
                'usuario': 'string'
        },
        'datetime_columns': [
                'data_hora_putaway'
        ],
        'encoding': 'utf-16',
        'sep': '\t'
    },
        'jornada' : {
        'remove_columns': [],
        'rename_columns': {
                'dia': 'data',
                'matricula': 'matricula',
                'cod': 'cod',
                'hora': 'hora'
        },
        'column_types': {
                'matricula': 'string',
                'cod': 'string',
        },
        'datetime_columns': [
                'data'
        ],
        'encoding': 'ascii',
        'sep': ';'
    },
        'padrao' : {
        'remove_columns': [],
        'rename_columns': {},
        'column_types': {},
        'datetime_columns': [],
        'encoding': 'utf-16',
        'sep': '\t'
    },
}
