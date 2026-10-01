'''
import pandas as pd 
import datetime as dt 
df = pd.read_excel('tabela_vendas_ZePequeno_corrigido.xlsx')

#1
df['Data'] = pd.to_datetime(df['Data'], dayfirst=True)
print(df.dtypes)

#2
df['Num_mes'] = df['Data'].dt.month
print(df.head())

#3
vendas_mes = df.groupby('Num_mes')['Valor_Venda'].sum().reset_index()
print(vendas_mes)

#4
df_trimestre = df[df['Num_mes'].isin([1, 2, 3])]
df_trimestre.to_excel("venda_primeiro_trimestre.xlsx", index=False)

#5
df["Dia_semana"] = df["Data"].dt.day_name()
ticket_medio_dia = df.groupby("Dia_semana")["Valor_Venda"].mean()
dia_maior_ticket = ticket_medio_dia.idxmax()
print(dia_maior_ticket)

#6
data_hoje = dt.datetime.now()
data_limite = data_hoje - dt.timedelta(days=90)
vendas_recentes = df[df['Data'] >= data_limite]
print(len(vendas_recentes))
'''
'''
def calcula_nota(nota1, nota2):
    media = (float(notas1)+float(notas2))/2
    return print(f"{media}")

nota1 = input("nota 1")
nota2 = input("nota 2")
calcula_nota(nota1, nota2)
'''
'''
def fazer_for():
    valor = 0
    for i in range(5):
        valor += 1
        if condição:
            return valor
    return x

print(fazer_for())
'''
'''
meta = 10000
vendas = {
    "João":15000,
    "Julia":27000,
    "Marcus":9900,
    "Maria":3750,
    "Ana":10300,
    "Alon":7870
}

def calculo_meta(meta,vendas):
    bateram_meta = []
    for vendedor in vendas:
        if vendas[vendedor]>=meta:
            bateram_meta.append(vendedor)
    perc_baterammeta = len(bateram_meta)/len(vendas)
    return perc_baterammeta,bateram_meta

p_meta,vendedores_acima= calculo_meta(meta,vendas)
print(p_meta)
print(vendedores_acima)
'''

import pandas as pd 
df = pd.read_excel('tabela_vendas_ZePequeno_corrigido.xlsx')

def filtrar_por_regiao(dataframe, regiao):
    return dataframe[dataframe["Região"]==regiao]

def total_por_canal(dataframe,canal):
    filtrado = dataframe[dataframe["Canal"] == canal]
    return filtrado["Valor_Venda"].sum()

norte = filtrar_por_regiao(df,"Norte")
print(norte.head())

sul = filtrar_por_regiao(df,"Sul")
print(sul.head())

total_online = total_por_canal(df,"E-commerce")
print(f"Vendas Online totalizam em R${total_online:,.2f}")

