# Pipeline ETL - Dados Portuários (Paranaguá e Santos)

Este projeto implementa um pipeline **ETL (Extract, Transform, Load)** para coletar, tratar, analisar e armazenar dados de movimentação de navios dos portos de **Paranaguá** e **Santos**.

Todo o processo foi organizado no padrão **Medallion Architecture** (camadas **bronze**, **silver** e **gold**), o que facilita a manutenção, rastreabilidade e confiabilidade dos dados.  
Os resultados finais também foram carregados em uma **tabela SQL**, que permite consultas e visualização de forma mais prática.

---

## Fluxo do Processo

1. **Extração (Bronze)**  
   - Faz a requisição HTTP para as páginas dos portos.  
   - Verifica se a resposta foi bem-sucedida.  
   - Faz o parsing do HTML com **BeautifulSoup**.  
   - Lê as tabelas da página com **pandas.read_html()**.  
   - Salva as tabelas de interesse como arquivos **CSV** na pasta `data/bronze`, mantendo o formato **idêntico ao site**.

2. **Transformação (Silver)**  
   - Lê os arquivos CSV da camada bronze.  
   - Pula a primeira linha (`skiprows=1`) pois contém cabeçalhos extras.  
   - Mantém apenas as colunas relevantes para análise.  
   - Concatena os dados (atracados e despachados).  
   - Salva um **único CSV normalizado** na pasta `data/silver`.

3. **Normalização e Enriquecimento (Gold)**  
   - Lê os arquivos da camada silver para ambos os portos.  
   - Adiciona a coluna `porto` para identificar a origem.  
   - Unifica colunas equivalentes (por exemplo, `Sentido` / `Operaç Operat`) para padronização.    
   - Adiciona a coluna `data_execucao` com a data/hora da execução do script.  
   - Exclui colunas redundantes e ordena as colunas para facilitar a análise.  
   - Salva o resultado final como **CSV** na pasta `data/gold`.

4. **Carga no Banco de Dados (SQL)**  
   - Os dados processados são carregados em uma tabela SQL, definida no arquivo de script da pasta `database_scripts`.  
   - Foi criada uma **única tabela consolidada** no banco, facilitando a visualização e as análises posteriores.

---

## 📂 Estrutura do Projeto

navio_pipeline/

data:

    - bronze/ CSVs extraídos do site (brutos)
    - silver/ CSVs normalizados
    - gold/ CSV final pronto para análises
database:
    
    - database.py/ Scripts e conexão com o banco/Configuração da conexão com SQL

database_scripts:

    - script.sql/ Script para criar tabela no banco

root:

    - main.py/ Arquivo principal que orquestra as funções

medallion:

    - bronze.py/ Lógica de extração
    - silver.py/ Lógica de limpeza e padronização
    - gold.py/ Lógica de unificação e carga

- requirements.txt: Dependências do projeto
- venv: Ambiente virtual 
- README.md: Este arquivo

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.12.10**
- [Pandas](https://pandas.pydata.org/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://requests.readthedocs.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Schedule](https://pypi.org/project/schedule/)
- VS Code como ambiente de desenvolvimento

---

## ⚙️ Instalação

1. Clone este repositório:
```bash
git clone https://github.com/jholsumback/pipeline_etl_veeries.git
cd pipeline_etl_veeries
```

2. Crie e ative o ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Configure o acesso ao banco no aquivo:
- database/database.py

## Execução do pipeline
- Execute o arquivo main.py para rodar todo o fluxo:
```bash
python main.py
```
📈 Observações Importantes

As saídas serão geradas automaticamente nas pastas bronze → silver → gold e no banco de dados.

A consolidação final foi feita em uma única tabela SQL, o que facilita consultas e visualização.

As camadas bronze, silver e gold permitem rastrear cada etapa do pipeline.

A padronização e a criação da coluna data_execucao garantem consistência histórica dos dados.

Optei por manter a coluna com a unidade original em MOVs (movimentos) em vez de convertê-la para toneladas (Tons), porque cada uma representa uma métrica distinta:

MOVs indicam o número de operações de embarque ou desembarque realizadas.

Tons representam o peso da carga movimentada.

Se eu convertesse os MOVs para toneladas, misturaria duas naturezas de informação diferentes contagem de operações vs. peso transportado, o que poderia causar confusão na interpretação dos dados.

Ao manter a métrica original, a tabela fica mais clara e coerente, permitindo análises separadas: por quantidade de operações (MOVs) ou por volume/peso (Tons), de acordo com a necessidade.

**Agendamento automático do pipeline**
O projeto utiliza a biblioteca schedule para automatizar a execução diária do pipeline ETL. O seguinte trecho de código garante que todo o processo de extração, transformação, agregação e carga dos dados seja executado automaticamente todos os dias às 09:00 (no arquivo main.py). Isso permite que o pipeline funcione de forma automática, sem necessidade de execução manual.

**Dicionário tabela SQL:**

- Coluna **sentido**: indica se a operação é de exportação ou importação (IMP/EXP), e Embarque e Desembarque (EMB/DESC).
- Coluna **produto**: especifica o tipo de produto que está sendo transportado.
- Coluna **navio**: informa o nome ou tipo do navio responsável pelo transporte.
- Coluna **porto**: identifica o porto de origem dos dados.
- Coluna **data_execucao**: registra a data e hora em que o script foi executado.
- Coluna **saldo total**: indica o volume total efetivamente carregado.
- Coluna **chegada**: indica a data e hora de chegada do navio ao porto.
