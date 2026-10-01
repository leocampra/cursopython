import pandas as pd 
df = pd.read_excel("tabela_vendas_ZePequeno_corrigido.xlsx")
'''
# 1
print(df.shape)

#2
resumo = df[["Região", "Valor_Venda"]]
resumo.to_csv("resumo_vendas.csv", index=False)
print(resumo.head())

#3
df_online = df[df['Canal'].astype(str).str.strip().str.lower() == 'e-commerce']
df_online.to_json("vendas.json", orient="records", force_ascii=False)
print("Quantidade de registros exportados", len(df_online))
'''

import pandas as pd 
'''
df = pd.read_excel("tabela_vendas_ZePequeno_corrigido.xlsx")

#1
print(df.head())
print("\nValor da primeira venda:", df["Valor_Venda"].iloc[0])

#2
print(df.dtypes)

#3
df.to_json(
    "vendas_completo.json",
    orient="records",       
    force_ascii=False,      
    indent=2                
)
print("Arquivo JSON salvo com sucesso!")
print(f"Total de registros no JSON: {len(df)}")

#4
df_resumo_original = df[["Região", "Valor_Venda"]].reset_index(drop=True)
df_csv = pd.read_csv("resumo_vendas.csv")

resultado = df_resumo_original.equals(df_csv)
print("Os DataFrames são idênticos?", resultado)

print("Shape do original:", df_resumo_original.shape)
print("Shape do CSV:     ", df_csv.shape)
print("Colunas original:", df_resumo_original.columns.tolist())
print("Colunas do CSV:  ", df_csv.columns.tolist())

#5
df = pd.read_excel(
    "tabela_vendas_ZePequeno_corrigido.xlsx",
    dtype={"Valor_Venda": float}
)

# Confirmar o tipo da coluna
print("Tipo de Valor_Venda:", df["Valor_Venda"].dtype)

# Calcular a soma total de vendas
soma_total = df["Valor_Venda"].sum()

# Exibir o resultado formatado
print(f"Soma total de vendas: R$ {soma_total:,.2f}")
'''
#6
# São Paulo é a única cidade do Sudeste presente.
# Adaptando o filtro para refletir a realidade dos dados:
cidades_sudeste = ["São Paulo"]
df_sudeste = df[df["Região"].isin(cidades_sudeste)]

# Verificar registros encontrados
print(f"Registros encontrados: {len(df_sudeste)}")
print(df_sudeste)

# Calcular a média de Valor_Venda
media_sudeste = df_sudeste["Valor_Venda"].mean()
print(f"\nMédia de Valor_Venda (São Paulo / Sudeste): R$ {media_sudeste:,.2f}")

# Exportar para Excel separado
df_sudeste.to_excel("vendas_sudeste.xlsx", index=False)
print("Arquivo exportado: vendas_sudeste.xlsx")
