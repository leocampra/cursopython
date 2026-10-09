import pandas as pd
import numpy as np

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
    nulos_restantes = df_limpo.isnull().sum().sum()
    print(f"Tratamento concluído. Nulos restantes: {nulos_restantes}")

    return df_limpo

# Uso
df_limpo = tratar_nulos(df)
print(df_limpo)

