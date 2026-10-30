'''
from pathlib import Path
import requests
caminho_ibge_url = "https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2025/POP2025_20260113.xls"
caminho_salvar = Path(r"relatorios/pop_ibge.xls")
print("Baixando arquivo do IBGE...")
resp = requests.get(caminho_ibge_url, stream=True, timeout=60)
resp.raise_for_status()
with open(caminho_salvar, "wb") as f:
    for chunk in resp.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)
print("Arquivo salvo em:", caminho_salvar)
print("Download concluído com sucesso!")
'''
from pathlib import Path
import pandas as pd
import requests

api_municipios_ibge = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

params = {
    "orderBy": "nome"
}

response = requests.get(api_municipios_ibge, params=params)
response.raise_for_status()  # Garante que a requisição foi bem-sucedida

dados_json = response.json()
df_completo = pd.json_normalize(dados_json)
colunas_desejadas = [
    'id', 
    'nome',
    'microrregiao.id', 
    'microrregiao.mesorregiao.UF.nome',
    'microrregiao.mesorregiao.UF.sigla',
    'microrregiao.mesorregiao.UF.regiao.nome'
]
df_filtrado = df_completo[colunas_desejadas]

df_ibge_filtrado = df_filtrado.rename(columns={
    'id': 'Código IBGE',
    'nome': 'Nome do Município',
    'microrregiao.id': 'Código da Microrregião',
    'microrregiao.mesorregiao.UF.nome': 'Nome do Estado',
    'microrregiao.mesorregiao.UF.sigla': 'Estado (UF)',
    'microrregiao.mesorregiao.UF.regiao.nome': 'Região'
})
caminho_salvar = Path(r"relatorios/municipios_ibge_filtrado.csv")

df_ibge_filtrado.to_csv(caminho_salvar, index=False, sep=";")
print("\n--- Visualização da Tabela Filtrada ---")

'''
df_ibge = pd.json_normalize(dados_json)

print("Endpoint utilizado:", response.url)

print(df_ibge.head())
print(df_ibge.columns.tolist())

caminho_salvar = Path(r"relatorios/municipios_ibge_simplificado.csv")

df_ibge.to_csv(caminho_salvar, index=False, sep=";")

print(f"Arquivo salvo com sucesso em: {caminho_salvar}")

'''
