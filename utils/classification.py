import numpy as np
import pandas as pd

def classify_setores_picking(df: pd.DataFrame) -> pd.Series:
    df['box'] = pd.to_numeric(df['box'], errors='coerce').fillna(-1).astype(int)

    cond = [
        (df['tipo_de_pedido'].isin(['S01 - ENTREGA A CLIENTES']) & df['box'].between(557,584)), # Fracionado Pesados
        (df['tipo_de_pedido'].isin(['S13 - ABASTECIMENTO DE LOJA BOA',
                                    'S14 - ABASTECIMENTO DE LOJA QEB',
                                    'S46 - ABASTECIMENTO RETIRA LOJA',
                                    'S48 - ABASTECIMENTO CEL RJ',
                                    'S11 - TRANSF. LOJA VIA DEPOSITO BOA']) & df['box'].between(595,638)), # EAD - Abastecimento de Lojas
        (df['tipo_de_pedido'].isin(['S13 - ABASTECIMENTO DE LOJA BOA',
                                    'S14 - ABASTECIMENTO DE LOJA QEB',
                                    'S46 - ABASTECIMENTO RETIRA LOJA',
                                    'S48 - ABASTECIMENTO CEL RJ',
                                    'S11 - TRANSF. LOJA VIA DEPOSITO BOA']) & df['box'].between(277,326)), # Polo - Abastecimento de Lojas
        (df['tipo_de_pedido'].isin(['S01 - ENTREGA A CLIENTES']) & ((df['box'].between(331,386)) | (df['box'].between(387,412)))), # Ribeirao Preto + Uberlandia
        (df['tipo_de_pedido'].isin(['S01 - ENTREGA A CLIENTES','S02 - RETIRA CLIENTE DEPOSITO']) & df['box'].between(413,556)), # Entrega Cliente + Polo-SP 
        (df['tipo_de_pedido'].isin(['S53 - TRANSFERENCIA ENTRE CDS']) & df['box'].between(595,638)), # EAD - Balanço
        (df['tipo_de_pedido'].isin(['S13 - ABASTECIMENTO DE LOJA BOA',
                                    'S14 - ABASTECIMENTO DE LOJA QEB',
                                    'S46 - ABASTECIMENTO RETIRA LOJA',
                                    'S48 - ABASTECIMENTO CEL RJ',
                                    'S11 - TRANSF. LOJA VIA DEPOSITO BOA'])), # Abastecimento de Lojas
        (df['tipo_de_pedido'].isin(['S01 - ENTREGA A CLIENTES','S02 - RETIRA CLIENTE DEPOSITO'])), # Ribeirao Preto + Uberlandia 2
        (df['tipo_de_pedido'].isin(['S53 - TRANSFERENCIA ENTRE CDS'])), # Balanço
        (df['tipo_de_pedido'].isin(['S05 - TRANSF EAD PROGRAMADA', 'S04 - TRANSF EAD AUTOMATICA'])), # EAD
        (df['tipo_de_pedido'].isin(["S39 - EXPEDICAO LEVES",
                                    "S39M - EXPEDICAO LEVES",
                                    "S39R - Single line",
                                    'S39P - EXPEDICAO LEVES',
                                    'S39I - EXPEDICAO LEVES'])) # Leves
    ]

    values = [
        'Fracionado Pesados',
        'EAD - Abastecimento de Lojas',
        'Polo - Abastecimento de Lojas',
        'Ribeirao Preto + Uberlandia',
        'Entrega Cliente + Polo-SP',
        'EAD - Balanco',
        'Abastecimento de Lojas',
        'Ribeirao Preto + Uberlandia',
        'Balanco',
        'EAD',
        'Leves'
    ]

    return np.select(cond, values, default='Outras Saidas')

def classify_setores(df: pd.DataFrame) -> pd.Series:
    df['box'] = pd.to_numeric(df['box'], errors='coerce').fillna(-1).astype(int)

    cond = [
        (df['tipo_de_pedido'].isin(['S01 - ENTREGA A CLIENTES']) & df['box'].between(557,584)),  # Fracionado Pesados
        (df['tipo_de_pedido'].isin(['S13 - ABASTECIMENTO DE LOJA BOA',
                                    'S14 - ABASTECIMENTO DE LOJA QEB',
                                    'S46 - ABASTECIMENTO RETIRA LOJA',
                                    'S48 - ABASTECIMENTO CEL RJ',
                                    'S11 - TRANSF. LOJA VIA DEPOSITO BOA']) & df['box'].between(595,638)),  # EAD - Abastecimento
        (df['tipo_de_pedido'].isin(['S13 - ABASTECIMENTO DE LOJA BOA',
                                    'S14 - ABASTECIMENTO DE LOJA QEB',
                                    'S46 - ABASTECIMENTO RETIRA LOJA',
                                    'S48 - ABASTECIMENTO CEL RJ',
                                    'S11 - TRANSF. LOJA VIA DEPOSITO BOA']) & df['box'].between(277,326)),  # Polo - Abastecimento
        (df['tipo_de_pedido'].isin(['S01 - ENTREGA A CLIENTES']) & ((df['box'].between(331,386)) | (df['box'].between(387,412)))),  # RP + Uberlandia
        (df['tipo_de_pedido'].isin(['S01 - ENTREGA A CLIENTES','S02 - RETIRA CLIENTE DEPOSITO']) & df['box'].between(413,556)),  # Entrega Cliente + Polo-SP
        (df['tipo_de_pedido'].isin(['S53 - TRANSFERENCIA ENTRE CDS']) & df['box'].between(595,638)),  # EAD - Balanço
        (df['tipo_de_pedido'].isin(['S13 - ABASTECIMENTO DE LOJA BOA',
                                    'S14 - ABASTECIMENTO DE LOJA QEB',
                                    'S46 - ABASTECIMENTO RETIRA LOJA',
                                    'S48 - ABASTECIMENTO CEL RJ',
                                    'S11 - TRANSF. LOJA VIA DEPOSITO BOA'])),  # Abastecimento de Lojas
        (df['tipo_de_pedido'].isin(['S01 - ENTREGA A CLIENTES','S02 - RETIRA CLIENTE DEPOSITO'])),  # RP + Uberlandia 2
        (df['tipo_de_pedido'].isin(['S53 - TRANSFERENCIA ENTRE CDS'])),  # Balanço
        (df['tipo_de_pedido'].isin(['S05 - TRANSF EAD PROGRAMADA', 'S04 - TRANSF EAD AUTOMATICA'])),  # EAD
        (df['tipo_de_pedido'].isin(["S39 - EXPEDICAO LEVES",
                                    "S39M - EXPEDICAO LEVES",
                                    "S39R - SINGLE LINE",
                                    'S39P - EXPEDICAO LEVES',
                                    'S39I - EXPEDICAO LEVES']))  # Leves
    ]

    values = [
        'Fracionado Pesados',
        'EAD - Abastecimento de Lojas',
        'Polo - Abastecimento de Lojas',
        'Ribeirao Preto + Uberlandia',
        'Entrega Cliente + Polo-SP',
        'EAD - Balanco',
        'Abastecimento de Lojas',
        'Ribeirao Preto + Uberlandia',
        'Balanco',
        'EAD',
        'Leves'
    ]

    return np.select(cond, values, default='Outras Saidas')

def cancel_classify_setores(df: pd.DataFrame) -> pd.Series:
    cond = [
        df['tipo_de_pedido'].isin(['S13 - ABASTECIMENTO DE LOJA BOA',
                                    'S14 - ABASTECIMENTO DE LOJA QEB',
                                    'S46 - ABASTECIMENTO RETIRA LOJA',
                                    'S48 - ABASTECIMENTO CEL RJ',
                                    'S11 - TRANSF. LOJA VIA DEPOSITO BOA',
                                    'S12 - TRANSF.LOJA VIA DEPOSITO QEB']), # Abastecimento de Lojas
        df['tipo_de_pedido'].isin(['S53 - TRANSFERENCIA ENTRE CDS']), # Balanço
        df['tipo_de_pedido'].isin(['S01 - ENTREGA A CLIENTES', 'S02 - RETIRA CLIENTE DEPOSITO']), # Entrega a Cliente
        df['tipo_de_pedido'].isin(['S05 - TRANSF EAD PROGRAMADA', 'S04 - TRANSF EAD AUTOMATICA']), # EAD
        df['tipo_de_pedido'].isin(["S39 - EXPEDICAO LEVES",
                                   "S39M - EXPEDICAO LEVES",
                                   "S39R - SINGLE LINE",
                                   'S39P - EXPEDICAO LEVES',
                                   'S39I - EXPEDICAO LEVES']) # Leves
    ]
    values = [
        'Abastecimento de Lojas',
        'Balanco',
        'Entrega a Cliente',
        'EAD',
        'Leves'
    ]
    return np.select(cond,values,default='Outras saidas')

def check_deadline(df: pd.DataFrame) -> pd.Series:

    deadline_1 = df['data_locacao_pedido'] + pd.Timedelta(days=1)
    deadline_1 = deadline_1.dt.normalize() + pd.Timedelta(hours=5, minutes=30)

    deadline_2 = df['data_locacao_pedido'] + pd.Timedelta(days=1)
    deadline_2 = deadline_2.dt.normalize() + pd.Timedelta(hours=10, minutes=0)

    deadline_3 = df['data_locacao_pedido'].dt.normalize() + pd.Timedelta(hours=23, minutes=30)

    deadline_4 = df['data_locacao_pedido'] + pd.Timedelta(days=1)
    deadline_4 = deadline_4.dt.normalize() + pd.Timedelta(hours=18, minutes=0)

    cond_status = df['status_olpn'] == 'Shipped'
    cond_data = df['data_locacao_pedido'].notna()
    cond_geral = cond_status & cond_data

    cond_box_1 = df['box'].between(413, 526)
    cond_prazo_1 = df['data_hora_ultimo_update_olpn'] <= deadline_1

    cond_box_2 = df['box'].between(527, 556)
    cond_prazo_2 = df['data_hora_ultimo_update_olpn'] <= deadline_2

    cond_box_3 = df['box'].between(331, 412)
    cond_prazo_3 = df['data_hora_ultimo_update_olpn'] <= deadline_3

    cond_box_4 = df['box'].between(557, 584)
    cond_prazo_4 = df['data_hora_ultimo_update_olpn'] <= deadline_4

    resultado = pd.Series(index=df.index, dtype='object', name='situacao_prazo')

    cond_1 = cond_geral & cond_box_1
    cond_2 = cond_geral & cond_box_2
    cond_3 = cond_geral & cond_box_3
    cond_4 = cond_geral & cond_box_4

    resultado[cond_1] = np.where(cond_prazo_1[cond_1], 'No prazo', 'Fora do prazo')
    resultado[cond_2] = np.where(cond_prazo_2[cond_2], 'No prazo', 'Fora do prazo')
    resultado[cond_3] = np.where(cond_prazo_3[cond_3], 'No prazo', 'Fora do prazo')
    resultado[cond_4] = np.where(cond_prazo_4[cond_4], 'No prazo', 'Fora do prazo')

    return resultado