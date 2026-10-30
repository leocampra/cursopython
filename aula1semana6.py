import pandas as pd
import numpy as np
from datetime import timedelta

data = {
    "Região":       ["Sul", "Norte", np.nan, "Leste", "Sul", np.nan, "Norte", "Leste", "Sul", "Norte"],
    "Valor_Venda":  [120.5, np.nan, 340.0, np.nan, 210.0, np.nan, np.nan, 180.0, np.nan, 95.0],
    "Categoria":    ["A", "B", np.nan, "A", np.nan, "B", "A", np.nan, "B", "A"],
    "Data_Pedido":  pd.to_datetime(["2024-01-01", np.nan, "2024-01-03", np.nan,
                                    "2024-01-05", "2024-01-06", np.nan, "2024-01-08",
                                    "2024-01-09", np.nan]),
    "Qtd_Itens":    [3, 1, np.nan, 4, np.nan, 2, np.nan, 5, 3, np.nan],
}

df = pd.DataFrame(data)

'''
# Percentual de nulos por coluna
percentual_nulos = df.isnull().mean() * 100

# Ordenando do maior para o menor
percentual_nulos = percentual_nulos.sort_values(ascending=False)
print("Percentual de valores ausentes por coluna:")
print(percentual_nulos.round(1))

# Colunas com mais de 30% de nulos
criticas = percentual_nulos[percentual_nulos > 30]
print("\nColunas com mais de 30% de valores ausentes:")
print(criticas)

# Imputação da mediana por grupo de Região
df["Valor_Venda"] = df.groupby("Região")["Valor_Venda"].transform(
    lambda x: x.fillna(x.median())
)

# Confirmação: se houver nulos restantes, o assert lança um erro
assert df["Valor_Venda"].isnull().sum() == 0, "Ainda existem nulos em Valor_Venda!"

print("Imputação concluída com sucesso.")

print(df[["Região", "Valor_Venda"]])

def tratar_nulos(df):
    df_limpo = df.copy()
    colunas_numericas = df_limpo.select_dtypes(include=["number"]).columns
    for col in colunas_numericas:
        df_limpo[col] = df_limpo[col].fillna(df_limpo[col].median())
    
    # Colunas categóricas → moda (valor mais frequente)
    colunas_categoricas = df_limpo.select_dtypes(include=["object"]).columns
    for col in colunas_categoricas:
        moda = df_limpo[col].mode()[0]  # mode() retorna uma Series; pegamos o primeiro
        df_limpo[col] = df_limpo[col].fillna(moda)

    # Colunas de data → forward fill
    colunas_data = df_limpo.select_dtypes(include=["datetime"]).columns
    for col in colunas_data:
        df_limpo[col] = df_limpo[col].ffill()

    # Verificação final
    nulos_restantes = df_limpo.isnull().sum()
    print(f"Tratamento concluído. Nulos restantes: {nulos_restantes}")

    return df_limpo

# Uso
df_limpo = tratar_nulos(df)
print(df_limpo)

#df = pd.read_excel ("tabela_vendas_ZePequeno_corrigido.xlsx")
#1
duplicadas = df.duplicated().sum()
print(duplicadas)

#2
if duplicadas == 0: 
    df = pd.concat([df, df.head()], ignore_index=True)
print(df.head)

#3
colunas = ['Canal', 'Produto', 'Data']
duplicatas_parciais = df[df.duplicated(subset=colunas, keep=False)]
contagem_canais = duplicatas_parciais.groupby('Canal').size()
mais_duplicadas = contagem_canais.idxmax()
print(mais_duplicadas)
'''
#4
data = {
    "Região":       ["Sul", "Norte", np.nan, "Leste", "Sul", np.nan, "Norte", "Leste", "Sul", "Norte"],
    "Valor_Venda":  [120.5, np.nan, 340.0, np.nan, 210.0, np.nan, np.nan, 180.0, np.nan, 95.0],
    "Categoria":    ["A", "B", np.nan, "A", np.nan, "B", "A", np.nan, "B", "A"],
    "Data_Pedido":  pd.to_datetime(["2024-01-01", np.nan, "2024-01-03", np.nan,
                                    "2024-01-05", "2024-01-06", np.nan, "2024-01-08",
                                    "2024-01-09", np.nan]),
    "Qtd_Itens":    [3, 1, np.nan, 4, np.nan, 2, np.nan, 5, 3, np.nan],
}

df = pd.DataFrame(data)
duplicadas = df.duplicated().sum()

if duplicadas == 0: 
    df = pd.concat([df, df.head()], ignore_index=True)

def marca_suspeitas_janela(df):
       df = df.sort_values(["Região", "Categoria", "Data_Pedido"]).copy()
       # compara com linha anterior
       prev_igual = (
           (df["Região"] == df["Região"].shift(1)) &
           (df["Categoria"] == df["Categoria"].shift(1)) &
           ( (df["Data_Pedido"] - df["Data_Pedido"].shift(1)).abs() <= timedelta(days=1) )
       )
       # compara com linha proxima
       next_igual = (
           (df["Região"] == df["Região"].shift(-1)) &
           (df["Categoria"] == df["Categoria"].shift(-1)) &
           ( (df["Data_Pedido"].shift(-1) - df["Data_Pedido"]).abs() <= timedelta(days=1) )
       )
       df["suspeita_janela_1dia"] = prev_igual | next_igual
       return df

print(marca_suspeitas_janela(df))














'''

total_duplicadas = df.duplicated().sum()
print(total_duplicadas)

if df.duplicated().sum() == 0:
    df = pd.concat([df, df.iloc[:5]], ignore_index=True)

print(df)

dup_parciais = df.duplicated(subset=["Região", "Categoria", "Data_Pedido"], keep=False)
df_dup = df[dup_parciais]
duplicatas_por_canal = df_dup.groupby("Região").size()
canal_com_mais_duplicatas = duplicatas_por_canal.idxmax()
print(canal_com_mais_duplicatas)

def marca_suspeitas_janela(df):
       df = df.sort_values(["Região", "Categoria", "Data_Pedido"]).copy()
       # compara com linha proxima
       prev_igual = (
           (df["Região"] == df["Região"].shift(1)) &
           (df["Categoria"] == df["Categoria"].shift(1)) &
           ( (df["Data_Pedido"] - df["Data_Pedido"].shift(1)).abs() <= timedelta(days=1) )
       )
       # compara com linha anterior
       next_igual = (
           (df["Região"] == df["Região"].shift(-1)) &
           (df["Categoria"] == df["Categoria"].shift(-1)) &
           ( (df["Data_Pedido"].shift(-1) - df["Data_Pedido"]).abs() <= timedelta(days=1) )
       )
       df["suspeita_janela_1dia"] = prev_igual | next_igual
       return df
print(marca_suspeitas_janela(df))
'''