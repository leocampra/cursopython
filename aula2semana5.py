import pandas as pd 
import datetime as dt
#1
df = pd.read_excel("tabela_vendas_ZePequeno_corrigido.xlsx")
'''
print(df.dtypes)
#2
produtos_valores = df[["Produto", "Valor_Venda"]]
produtos_valores.to_csv("produtos_valores.csv", index=False)
print(produtos_valores.head())
#3
df_csv = pd.read_csv("produtos_valores.csv", sep=";", encoding="utf-8")
print(df_csv.dtypes)
#4
df.to_json("vendas_completo.json", orient="records", force_ascii=False)
df_json = pd.read_json("vendas_completo.json")
print(df_json.head())
#5
def carregar_dados(caminho,tipo):
    if tipo == "excel":
        return pd.read_excel(caminho)
    elif tipo == "csv":
        return pd.read_csv(caminho)
    elif tipo == "json":
        return pd.read_json(caminho)
    else:
        raise ValueError("Tipo de arquivo não suportado. Use 'excel', 'csv' ou 'json'.")

print(carregar_dados("produtos_valores.csv", "doc").head())

#1
df_ecommerce = df[df['Canal'] == 'E-commerce']
print(df_ecommerce.head())

#2'
print(df.loc[:9, ['Produto', 'Valor_Venda']])

#3      
filtro_joinville = df[    
    (df['Região'].str.lower() == 'joinville') & 
    (df['Canal'] == 'Loja Física') & 
    (df['Valor_Venda'].between(1500, 2600))]
print(filtro_joinville)

vendas3 = df.query('Canal == "Loja Física" and Região == "Joinville" and Valor_Venda.between(1500, 2600)')
print(vendas3.head(10))

#4
vendas_2024 = df[df['Data'].dt.year == 2024]
total_vendas_2024 = vendas_2024['Valor_Venda'].sum()
print(f"Total vendido em 2024: R$ {total_vendas_2024:.2f}")

#5
for reg in df['Região'].unique():
    sub = df[df['Região'] == reg]
    medias = sub.groupby('Produto')['Valor_Venda'].mean()
    top_produto = medias.idxmax()
    print(f"{reg}: {top_produto}")
#5.1
col_regiao = "Região" if "Região" in df.columns else "Regiao"
col_valor = "Valor_Venda" if "Valor_Venda" in df.columns else "Valor_Venda"
df[col_regiao] = (
    df[col_regiao]
    .astype(str)
    .str.strip()
    .str.lower()
    .str.title()
)
media_prod_regiao = df.groupby([col_regiao, "Produto"])[col_valor].mean().reset_index()
idx_max = media_prod_regiao.groupby(col_regiao)[col_valor].idxmax()
top_produtos = media_prod_regiao.loc[idx_max]
print(top_produtos)

#6
media = df['Valor_Venda'].mean()
std   = df['Valor_Venda'].std()
outliers = df[df['Valor_Venda'] > media + 2*std]
print(f"Outliers encontrados: {len(outliers)}")

#1
Vendas_regiao = df.groupby('Região')['Valor_Venda'].sum().sort_values(ascending=False)
print(Vendas_regiao)

#2
vendas_regiao = df.groupby(['Canal'])['Valor_Venda'].agg([
    ('Qtd_Registros', 'count'),
    ('Total_Faturado', 'sum'),
    ('Valor_Medio', 'mean')
]).round(2)
print (vendas_regiao)

#3
vendas = df.groupby(['Região','Canal'])['Valor_Venda'].sum().sort_values(ascending=True)
print(vendas)

#4
vendas_regiao = df.groupby(['Região','Produto'])['Valor_Venda'].agg([
    ('Qtd_Registros', 'count'),
    ('Total_Faturado', 'sum'),
    ('Valor_Medio', 'mean')
]).round(2)
print (vendas_regiao)

#5
totais = df.groupby('Região')['Valor_Venda'].sum()
max_total = totais.max()
top_regioes = totais[totais == max_total]
print(top_regioes)
'''
#6
ranking_canais = (
    df.groupby('Canal')
      .agg(
          total=('Valor_Venda', 'sum'),
          media=('Valor_Venda', 'mean'),
          qtd  =('Valor_Venda', 'count')
      )
      .sort_values('media', ascending=False)
)
print(ranking_canais)