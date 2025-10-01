import pandas as pd
import os
from datetime import datetime

DATA_DIR = "data"
BRONZE = os.path.join(DATA_DIR, "bronze")
SILVER = os.path.join(DATA_DIR, "silver")

def normalize_paranagua_data():
    """
    Lê os arquivos extraídos da camada bronze e pula a primeira linha (skiprows=1) porque contém cabeçalhos extras,
    Mantém apenas as colunas relevantes para análise, concatena os dois dataframes (atracados e despachados),
    salva o resultado na camada silver.
    Returns: None

    """
    df_atracados = pd.read_csv(os.path.join(BRONZE, "porto_paranagua_atracados.csv"), skiprows=1)
    df_despachados = pd.read_csv(os.path.join(BRONZE, "porto_paranagua_despachados.csv"), skiprows=1)
    colunas_desejadas_atracados = ['Sentido', 'Mercadoria', 'Embarcação', 'Chegada', 'Previsto', 'Saldo Total']
    colunas_desejadas_despachados = ['Sentido', 'Mercadoria', 'Embarcação', 'Chegada', 'Previsto' ] 
    df_filtrados_atracados = df_atracados[colunas_desejadas_atracados]
    df_filtrados_despachados = df_despachados[colunas_desejadas_despachados]
    df_combined = pd.concat([df_filtrados_atracados, df_filtrados_despachados], ignore_index=True)
    df_combined.to_csv(os.path.join(SILVER, "porto_paranagua_silver.csv"), index=False)

def normalize_santos_data():
    """
    Lê todos os arquivos CSV na pasta bronze que correspondem às tabelas do porto de santos,
    pula a primeira linha (skiprows=1) porque contém cabeçalhos extras,
    concatena todos os dataframes em um único dataframe,
    mantém apenas as colunas relevantes para análise,
    salva o resultado na camada silver.

    Returns: None
    """
    all_files = [f for f in os.listdir(BRONZE) if f.startswith("porto_santos_table_") and f.endswith(".csv")]
    dfs = [pd.read_csv(os.path.join(BRONZE, f), skiprows=1) for f in all_files]
    df_combined = pd.concat(dfs, ignore_index=True)
    colunas_desejadas = ['Navio Ship', 'Cheg/Arrival d/m/y', 'Operaç Operat', 'Mercadoria Goods', 'Peso Weight']
    df_final = df_combined[colunas_desejadas]
    df_final.to_csv(os.path.join(SILVER, "porto_santos_silver.csv"), index=False)