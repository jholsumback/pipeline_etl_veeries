import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

DATA_DIR = "data"
BRONZE = os.path.join(DATA_DIR, "bronze")

def extract_data_from_paranagua(url):
    """
    Faz a requisição à URL e verifica se a resposta foi bem-sucedida,
    faz o parsing do HTML com BeautifulSoup,
    lê todas as tabelas da página usando pandas,
    salva apenas as tabelas de interesse nos arquivos da camada bronze, no caso do 1 e 7 é por causa da localização das tabelas na página
    
    Keyword arguments: 
    url -- url do site do porto de paranagua
    Returns: None
    """ 
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return None
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    dfs = [pd.read_html(str(table))[0] for table in tables] 
    dfs[1].to_csv(os.path.join(BRONZE, "porto_paranagua_atracados.csv"), index=False)
    dfs[7].to_csv(os.path.join(BRONZE, "porto_paranagua_despachados.csv"), index=False)


def extract_data_from_santos(url):
    """
    Faz a requisição à URL e verifica se a resposta foi bem-sucedida, faz o parsing do HTML com BeautifulSoup, 
    lê todas as tabelas da página usando pandas, Salva todas as tabelas encontradas na página do porto de santos

    Keyword arguments:
    url -- url do site do porto de santos
    Returns: None
    """
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return None
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')
    dfs = [pd.read_html(str(table))[0] for table in tables]
    for i, df in enumerate(dfs): 
        df.to_csv(os.path.join(BRONZE, f"porto_santos_table_{i}.csv"), index=False)