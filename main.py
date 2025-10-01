from medallion.bronze import extract_data_from_paranagua, extract_data_from_santos
from medallion.silver import normalize_paranagua_data, normalize_santos_data
from medallion.gold import normalize_gold_data
from database.database import save_to_database
import os
import schedule
import time

DATA_DIR = "data"
BRONZE = os.path.join(DATA_DIR, "bronze")
SILVER = os.path.join(DATA_DIR, "silver")
GOLD = os.path.join(DATA_DIR, "gold")
os.makedirs(BRONZE, exist_ok=True)
os.makedirs(SILVER, exist_ok=True)
os.makedirs(GOLD, exist_ok=True)

def run():
    """Orquestra todo o pipeline de ETL:
    - Extrai dados dos portos de Paranaguá e Santos (camada bronze)
    - Normaliza os dados extraídos (camada silver)
    - Unifica e padroniza os dados (camada gold)
    - Salva os dados finais no banco de dados PostgreSQL
    Returns: None
    """
    extract_data_from_paranagua("https://www.appaweb.appa.pr.gov.br/appaweb/pesquisa.aspx?WCI=relLineUpRetroativo")
    extract_data_from_santos("https://www.portodesantos.com.br/informacoes-operacionais/operacoes-portuarias/navegacao-e-movimento-de-navios/navios-esperados-carga")
    normalize_paranagua_data()
    normalize_santos_data()
    normalize_gold_data()
    save_to_database()

schedule.every().day.at("09:00").do(run)
while True:
    schedule.run_pending()
    time.sleep(3600)

