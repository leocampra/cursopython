import pandas as pd
import datetime as dt
from statistics import mean
import os

df = pd.read_excel('tabela_vendas_ZePequeno_corrigido.xlsx')

'''
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


#1
acima_da_media = lambda valor: valor > 284.84
print(acima_da_media(200.00))

#2
vendas = [900, 1200, 2991]
vendas_com_frete = list(map(lambda valor: valor + 100, vendas))
print(vendas_com_frete)

#3
def categorizar_pacoca(Valor_Venda):
    if Valor_Venda >= 2000.00:
        return "Cx 100 Paçoca Premium"
    elif Valor_Venda >= 1500:
        return "Cx 100 Paçoca Free Sugar"
    else:
        return "Cx 100 Paçoca Padrão"

df["categoria"] = df["Valor_Venda"].apply(categorizar_pacoca)
print(df.head())

#3.1
df["categoria"] = df["Valor_Venda"].apply(
    lambda v: "Cx 100 Paçoca Premium" if v >= 2000 
    else ("Cx 100 Paçoca Free Sugar" if v >= 1500 else "Cx 100 Paçoca Padrão")
)
print(df.head())

#4
import json
registros = df.to_dict(orient="records")
registros_filtrados = list(
    filter(lambda r: r["Canal"] == "E-commerce" and r["Valor_Venda"] > 2000, registros)
)
print(json_debugs(registros_filtrados))

#4.1
df_filtrado = df[(df["Canal"] == "E-commerce") & (df["Valor_Venda"] > 2000)]
print(df_filtrado.head())

#4.2
registros = [
    ("E-Commerce", 2500),
    ("Loja Física", 3000),
    ("E-Commerce", 1500),
    ("E-Commerce", 4200),
]
vendas_filtradas = list(
    filter(lambda x: x[0] == "E-Commerce" and x[1] > 2000, registros)
)

print(vendas_filtradas)

#5
amplitude_vendas = df.groupby("Região")["Valor_Venda"].agg(lambda x: x.max() - x.min())
print(amplitude_vendas)

#6
df_ordenado = df.sort_values(
    by=["Região", "Valor_Venda"],
    ascending=[True, False],
    key=lambda coluna: coluna.str.lower() if coluna.dtype == "object" else coluna
)
print(df_ordenado)

#1
print(mean([900, 1500, 2991, 2084]))

#2
print(os.getcwd())
print(os.path.exists("tabela_vendas_ZePequeno_corrigido.xlsx"))

#3
import filtros_vendas
print(filtros_vendas.por_canal(df, "E-commerce").head())

#4
from pathlib import Path
[print(f.stem) for f in Path("relatorios/").glob("*.xlsx")]

#5
import json
def gerar_relatorio(df):
    relatorio = (
        df.groupby("Região")["Valor_Venda"]
        .agg(["sum","mean","min","max"])
        .to_dict()
    )
    return relatorio
print(json.debugs(gerar_relatorio(df)))
'''
#6
from filtros_vendas import *

print(filtros_vendas.funcao_publica1())
print(filtros_vendas.funcao_publica2())
print(filtros_vendas.funcao_interna())

