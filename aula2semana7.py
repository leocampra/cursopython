'''
from pathlib import Path  # Manipula caminhos de arquivos e diretórios de forma orientada a objetos.
import pandas as pd  # Manipula e analisa dados estruturados por meio de DataFrames e Series.
import requests  # Realiza requisições HTTP para consumir APIs e acessar recursos da web.

# CONFIGURAÇÕES

# Endpoint da API do Banco Central (OData)
# DataBase='202501' corresponde a janeiro de 2025
api_pix_bc = (
    "https://olinda.bcb.gov.br/olinda/servico/"
    "Pix_DadosAbertos/versao/v1/odata/"
    "TransacoesPixPorMunicipio(DataBase='202501')"
)

# Parâmetros da requisição
PARAMS = {"$format": "json", "$top": 1_000_000, "$filter":"Nome eq 'João'"}

# Caminho de salvamento ajustado para a extensão .xlsx conforme solicitado
caminho_salvar = Path(r"relatorios/pix_bancocentral.xlsx")

# Cria as pastas do caminho caso elas ainda não existam no computador
caminho_salvar.parent.mkdir(parents=True, exist_ok=True)

# EXECUÇÃO

print("Buscando dados de transações Pix por município...")

response = requests.get(api_pix_bc, params=PARAMS, timeout=30)
response.raise_for_status()

# O conteúdo principal do OData está na chave "value"
dados = response.json()["value"]

# Converte os dados brutos recebidos para um DataFrame do Pandas
df = pd.DataFrame(dados)

# Salva o DataFrame diretamente em formato Excel (.xlsx)
# Nota: Certifique-se de ter a biblioteca 'openpyxl' instalada (pip install openpyxl)
df.to_excel(caminho_salvar, index=False)

print("Arquivo Excel salvo em:", caminho_salvar)

# Fim do script
'''
'''
import pandas as pd
import requests

# 1. O Endpoint específico para Transações por Município
# Note que a DataBase já vai direto na estrutura da URL da API do BCB
url = (
    "https://olinda.bcb.gov.br/olinda/servico/"
    "Pix_DadosAbertos/versao/v1/odata/"
    "TransacoesPixPorMunicipio(DataBase='202501')"
)

# 2. Configurando as nossas ESCOLHAS (Parâmetros)
params = {
    "$format": "json",  # Queremos o resultado em formato JSON
    "$top": 100,  # Vamos trazer apenas as primeiras 100 linhas para testar
    # Queremos ordenar o resultado pelo nome do Município de forma ascendente (A-Z)
    "$filter": "Estado eq 'MINAS GERAIS'"
} # p.s: Vou verificar ese filtro pois esta dando erro na página do BC.

# 3. Fazendo a requisição
response = requests.get(url, params=params)
response.raise_for_status()

# 4. Capturando o RESULTADO enviado pelo Banco Central
dados_brutos = response.json()["value"]
df_pix = pd.DataFrame(dados_brutos)

# 5. Manipulando as colunas do RESULTADO que a documentação nos prometeu
print("Campos que vieram na tabela:", df_pix.columns.tolist())

# Exibindo apenas o Município e o Valor total pago por Pessoas Físicas (PF)
colunas_analise = ["Municipio", "Estado", "VL_PagadorPF"]
print(df_pix[colunas_analise].head())
'''

from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import requests

url = "https://books.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response, "html.parser")

titulo = soup.find('h3').get_text()

print(titulo)
