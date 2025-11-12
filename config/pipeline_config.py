from config.paths import ENV_PATH
from dotenv import load_dotenv
import os
from utils.config_logger import setup_logger

logger = setup_logger(__name__)

load_dotenv(dotenv_path=ENV_PATH)
EMAIL = os.getenv('LOGIN_EMAIL')
PASSWORD = os.getenv('LOGIN_PASSWORD')

CHUNKSIZE = 500_000

LINKS = {
    'LOGIN_ESTOQUE_MOV': 'link',
    'LOGIN_CSI': 'https://viavp-sci.sce.manh.com/bi/?perspective=home',
    'LOGIN_OLPN' : 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=i79E326D8D72B45F795E0897FCE0606F6&objRef=i79E326D8D72B45F795E0897FCE0606F6&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22i79E326D8D72B45F795E0897FCE0606F6%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%223.11%20-%20Status%20Wave%20%2B%20oLPN%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D',
    'LOGIN_CANCEL': 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=iD732BE4B1DA6487F8ACD69248DA2CC19&objRef=iD732BE4B1DA6487F8ACD69248DA2CC19&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22iD732BE4B1DA6487F8ACD69248DA2CC19%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%226.10%20-%20Pedidos%20Cancelados%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D',
    'LOGIN_PICKING': 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=iC20581CB9B43482BB800469299636529&objRef=iC20581CB9B43482BB800469299636529&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22iC20581CB9B43482BB800469299636529%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%224.05%20-%20Relat%C3%B3rio%20de%20Produtividade%20-%20Picking%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D',
    'LOGIN_PUTAWAY': 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=i1C7595C381DC48EF9311843A1F5ED5F3&objRef=i1C7595C381DC48EF9311843A1F5ED5F3&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22i1C7595C381DC48EF9311843A1F5ED5F3%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%226.15%20-%20Produtividade%20-%20Outbound%20Putaway%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D',
    'LOGIN_PACKING': 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=i3E96C0044C974F60ABC41F536196806B&objRef=i3E96C0044C974F60ABC41F536196806B&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22i3E96C0044C974F60ABC41F536196806B%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%225.03%20-%20Produtividade%20de%20Packing%20-%20Packed%20por%20hora%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D',
    'LOGIN_LOADING': 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=i27370057698144858929E8CB9D90181A&objRef=i27370057698144858929E8CB9D90181A&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22i27370057698144858929E8CB9D90181A%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%225.04%20-%20Produtividade%20Load%20-%20Load%20por%20hora%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D',
    'LOGIN_EXPEDICAO': 'https://viavp-sci.sce.manh.com/bi/?perspective=authoring&id=i14E08EF0A3D244EFAA7EFEA25F910A54&objRef=i14E08EF0A3D244EFAA7EFEA25F910A54&action=run&format=CSV&cmPropStr=%7B%22id%22%3A%22i14E08EF0A3D244EFAA7EFEA25F910A54%22%2C%22type%22%3A%22report%22%2C%22defaultName%22%3A%226.06%20-%20Expedi%C3%A7%C3%A3o%20-%20CD%22%2C%22permissions%22%3A%5B%22execute%22%2C%22read%22%2C%22traverse%22%5D%7D'
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
        'expedicoes':{
        'remove_columns': [
            'Data integração WMS',
            'Inventory Type ID',
            'Wave',
            'Pedido de venda',
            'Bandeira',
            'Status do pedido',
            'Destinatário',
            'CEP destinatário',
            'Cidade',
            'Estado',
            'Item',
            'Descrição do item',
            'Código do Setor',
            'Empresa',
            'Status da Nota Fiscal',
            'Shipment',
            'Marcação de EAD',
            'Ship Via',
            'Descrição',
            'UF',
            'Data Prometida',
            'Data Prevista Entrega',
            'Data Limite Expedição'
        ],
        'rename_columns': {
            'Data ultima movimentação':'dt_ultima_movimentacao',
            'Filial':'filial',
            'Pedido':'pedido',
            'Box':'box',
            'Tipo do pedido':'tipo_de_pedido',
            'Descrição':'descricao',
            'Setor do item':'setor_item',
            'Status':'status',
            'Qtde. original':'qtd_pcs_solicitada',
            'Qtde. Expedida':'qtd_pcs_expedida'
        },
        'column_types': {
            'filial':'string',
            'pedido':'string',
            'box':'Int64',
            'tipo_de_pedido':'string',
            'descricao':'string',
            'setor_item':'string',
            'status':'string',
            'qtd_pcs_solicitada':'Int64',
            'qtd_pcs_expedida':'Int64'
        },
        'datetime_columns': [
            'dt_ultima_movimentacao'
        ],
        'encoding':'utf-16',
        'sep':'\t'
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
                'Shipment',
                'Filial Destino',
                'Status Pedido',
                'Pedido de Venda',
                'Wave',
                'Descrição'
        ],
        'rename_columns': {
                'Filial': 'filial',
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
                'Filial':'filial',
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
                'Filial':'filial',
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
                'Filial':'filial',
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
        'loading' : {
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
                'Data',
                'Status',
                'DESCRIÇÃO ITEM',
                'Item Attribute1',
                'Transaction Type',
                'Inventory Type ID'
        ],
        'rename_columns': {
                'Filial':'filial',
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
                'matricula': 'Int64',
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