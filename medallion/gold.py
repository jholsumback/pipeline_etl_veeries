import pandas as pd
import os   
from datetime import datetime

DATA_DIR = "data"
SILVER = os.path.join(DATA_DIR, "silver")
GOLD = os.path.join(DATA_DIR, "gold")

def normalize_gold_data():
    """
    Lê os arquivos normalizados da camada silver para os portos de Paranaguá e Santos,
    adiciona uma coluna 'Porto' para identificar a origem dos dados,
    unifica as colunas equivalentes dos dois portos para padronizar os nomes usados no dataset final,
    adiciona uma coluna 'Data_Execucao' com a data e hora da execução do script,
    exclui as colunas que não são mais necessárias após a unificação
    ordena as colunas para melhor visualização
    salva o resultado na camada gold.

    Returns: None
    """
    df_paranagua = pd.read_csv(os.path.join(SILVER, "porto_paranagua_silver.csv"))
    df_santos = pd.read_csv(os.path.join(SILVER, "porto_santos_silver.csv"))
    df_paranagua['Porto'] = 'Paranaguá'
    df_santos['Porto'] = 'Santos'
    df_gold = pd.concat([df_paranagua, df_santos], ignore_index=True)
    data_execucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_gold['Data_Execucao'] = data_execucao
    df_gold['sentido'] = df_gold['Sentido'].fillna(df_gold['Operaç Operat'])
    df_gold['produto'] = df_gold['Mercadoria'].fillna(df_gold['Mercadoria Goods'])
    df_gold['navio'] = df_gold['Embarcação'].fillna(df_gold['Navio Ship'])
    df_gold['chegada'] = df_gold['Chegada'].fillna(df_gold['Cheg/Arrival d/m/y'])
    df_gold['saldo_total'] = df_gold['Saldo Total'].fillna(df_gold['Peso Weight'])
    
    df_gold = df_gold.drop(columns=[
        'Sentido', 'Operaç Operat',
        'Mercadoria', 'Mercadoria Goods',
        'Embarcação', 'Navio Ship',
        'Chegada', 'Cheg/Arrival d/m/y',
        'Peso Weight', 'Saldo Total','Previsto'
    ])
    df_gold.columns = [c.lower().strip() for c in df_gold.columns]
    cols = ['sentido', 'produto', 'navio', 'porto', 'data_execucao'] + [c for c in df_gold.columns if c not in ['sentido', 'produto', 'navio', 'porto', 'data_execucao']]
    df_gold = df_gold[cols]
    df_gold.to_csv(os.path.join(GOLD, "porto_gold.csv"), index=False)