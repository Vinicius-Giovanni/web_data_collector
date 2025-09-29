from utils.get_info import today, yesterday, business_date

todays = today()
yesterdays = yesterday()
business_dates = business_date()

MOTIVOS_OFICIAIS = {
    1: 'MOTIVO DESCONTINUADO (OUTROS)',
    2: 'DIVERGENCIA DE SALDO COM PCOM x WMS',
    3: 'PENDENCIA DE ARMAZENAGEM',
    4: 'ENDEREÇO VAZIO',
    5: 'NF SEM TRATAMENTO',
    6: 'LEITURA IMEI',
    7: 'ERRO OPERACIONAL',
    8: 'AVARIA',
    9: 'AVARIA/EAD',
    10: 'SALDO INSUFICIENTE',
    11: 'FALTA EAD',
    12: 'TRANSPORTADORA DECLINADA',
    13: 'SKU DIVERGENTE',
    14: 'PROGRAMACAO INDEVIDA',
    15: 'ILPN VOANDO',
    16: 'EXCESSO DE CUBAGEM',
    17: 'DTF RETORNO',
    18: 'FALTA DE COMPOSICAO',
    19: 'FALTA/CROSS',
    20: 'AVARIA/CROSS',
    21: 'CARRETA EM POSTO FISCAL',
    22: 'CARRETA NO SHOW',
    23: 'PEDIDO SEM TRACKING NUMBER',
    24: 'CRL/BARRAR ENTREGA',
    25: 'IE NAO CADASTRADA NA REGIAO',
    26: 'ERRO DE CEP',
    27: 'SOLICITACAO GESTAO'
}

MAPEAMENTO_TEXTUAL = {
    2: [r'diver[g|n]encia.*saldo.*pcom.*wms'],
    3: [r'pend[e|a]ncia.*armazen'],
    4: [r'endere[çc]o.*vazio'],
    5: [r'nf.*sem.*trat'],
    6: [r'imei'],
    7: [r'erro.*(operacional|armazenagem)'],
    8: [r'^avaria$'],
    9: [r'avaria.?/?ead'],
    10: [r'saldo.*insuf'],
    11: [r'falta.*ead'],
    12: [r'transportadora.*declinada|transportadora.*nao atende'],
    13: [r'sku.*diverg'],
    14: [r'programa[çc][aã]o.*ind'],
    15: [r'ilpn.*voando|lpn.*voando'],
    16: [r'excesso.*cubagem|cubagem.*excesso'],
    17: [r'dtf.*retorno'],
    18: [r'falta.*composi'],
    19: [r'cross'],
    20: [r'avaria.*cross'],
    21: [r'posto.*fiscal'],
    22: [r'no show'],
    23: [r'sem.*tracking'],
    24: [r'barrar.*entrega|crl'],
    25: [r'ie.*n[aã]o.*cadast'],
    26: [r'erro.*cep'],
    27: [r'solicita.*gest[aã]o'],
    1: [r'outro|outros']
}

REGRAS_DIRETAS = [
        (6, ['imei']),
        (5, ['nf', 'nota fiscal']),
        (4, ['endereco', 'vazio']),
        (14, ['progamacao indevida']),
        (3, ['armazenagem']),
        (2, ['wms'], ['pcom', 'saldo', 'x']),
        (10, ['saldo']),
        (27, ['gerente', 'autorizado', 'solicitado']),
        (18, ['composicao', 'composic']),
        (16, ['cubagem', 'problema de volume', 'nao coube', 'excesso']),
        (24, ['cliente'], ['nao quis', 'recusou', 'recusa']),
        (22, ['no show', 'nao apareceu']),
        (21, ['posto fiscal', 'parado na receita']),
]