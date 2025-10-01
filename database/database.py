from sqlalchemy import create_engine
import pandas as pd
import os
from datetime import datetime

DATA_DIR = "data"
GOLD = os.path.join(DATA_DIR, "gold")

def save_to_database():
    """
    Salva os dados da camada gold no banco de dados PostgreSQL,
    utilizando SQLAlchemy para a conexão e pandas para a inserção dos dados.
    Configura os parâmetros de conexão com o banco de dados (usuário, senha, host, porta, nome do banco).
    Lê o arquivo CSV da camada gold e insere os dados na tabela 'porto_data', sobrescrevendo a tabela se ela já existir.
    
    Returns: None
    """
    db_user = 'postgres'
    db_password = '12323'
    db_host = 'localhost'
    db_port = '5432'
    db_name = 'base_dados_teste_veeries'
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    df_gold = pd.read_csv(os.path.join(GOLD, "porto_gold.csv"))
    df_gold.to_sql('porto_data', engine, if_exists='append', index=False)