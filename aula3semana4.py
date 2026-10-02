import pandas as pd
import datetime as dt

df = pd.read_excel('tabela_vendas_ZePequeno_corrigido.xlsx')

#1
def saudar_vendedor(nome):
    print(f"Olá, {nome} boas vindas ao sistema de vendas Zé Pequeno.")

saudar_vendedor("Carlos")
saudar_vendedor("Mariana")
saudar_vendedor("Lucas")

#2
def total_lista(valores):
    return sum(valores)

vendas = [1200, 3400, 870, 2100, 950]
print(total_lista(vendas))

#3
def filtrar_canal(df, canal="E-commerce"):
    filtrado = df[df["Canal"] == canal]
    return filtrado["Valor_Venda"].sum()

print(filtrar_canal(df))
print(filtrar_canal(df, "Loja Física"))
print(filtrar_canal(df, "Atacado"))

#4
def comparar_regioes(df, *regioes):
    resultados = {}
    for regiao in regioes:
        total = df[df["Região"] == regiao]["Valor_Venda"].sum()
        resultados[regiao] = total
    for reg, val in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
        print(f"{reg}: R$ {val:,.2f}")

comparar_regioes(df, "Norte", "Sul", "Sudeste", "Centro-Oeste")

#5
def pipeline_vendas(df, **filtros):
    df_f = df.copy()
    for coluna, valor in filtros.items():
        df_f = df_f[df_f[coluna] == valor]
    total    = df_f["Valor_Venda"].sum()
    media    = df_f["Valor_Venda"].mean()
    contagem = len(df_f)
    top_prod = df_f.groupby("Produto")["Valor_Venda"].sum().idxmax()
    print(f"{total} {media} {contagem} {top_prod}")

pipeline_vendas(df,Canal="E-commerce",Região="Joinville")

#6
def analise_temporal(df, ano, mes=None):
    df["Data"] = pd.to_datetime(df["Data"])
    mask = df["Data"].dt.year == ano
    if mes:
        mask = df["Data"].dt.month == mes
    periodo = df[mask]
    total   = periodo["Valor_Venda"].sum()
    canal   = periodo.groupby("Canal")["Valor_Venda"].sum().idxmax()
    regiao  = periodo.groupby("Região")["Valor_Venda"].sum().idxmax()
    print(f"{total} {canal} {regiao}")

analise_temporal(df,2025)
