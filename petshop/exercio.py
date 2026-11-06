from pathlib import Path
import sqlite3

import pandas as pd
import datetime as dt

# Troque pelo caminho do banco no seu computador
caminho_banco = Path("/home/leonardo/leoteste/petshop.sqlite")

if not caminho_banco.exists():
    raise FileNotFoundError(f"Banco não encontrado: {caminho_banco}")

conexao = sqlite3.connect(caminho_banco)
clientes = pd.read_sql_query("SELECT * FROM clientes", conexao)
itens = pd.read_sql_query("SELECT * FROM itens", conexao)
unidades = pd.read_sql_query("SELECT * FROM unidades", conexao)
vendas = pd.read_sql_query("SELECT * FROM vendas", conexao)
itens_venda = pd.read_sql_query("SELECT * FROM itens_venda", conexao)
conexao.close()
'''
#1
produtos = itens[itens["tipo"] == "produto"].copy()
produtos["preco_novo"] = (produtos["preco_atual"] * 1.10).round(2)

resultado = produtos[["nome", "preco_atual", "preco_novo"]].sort_values(
    "preco_novo", ascending=False
)
print(resultado)
'''
'''
#2
itens_categoria = itens[["item_id", "categoria"]]
base = itens_venda.merge(vendas, on="venda_id").merge(itens_categoria, on="item_id")
base = base[base["status"] == "concluida"].copy()
base["faturamento"] = base["quantidade"] * base["preco_unitario"] - base["desconto"]
categorias = base.groupby("categoria", as_index=False).agg(
    quantidade=("quantidade", "sum"),
    faturamento=("faturamento", "sum"),
)
categorias["participacao"] = categorias["faturamento"] / categorias["faturamento"].sum() * 100
print(categorias.round(2).sort_values("faturamento", ascending=False))
'''
'''
#3
base = itens_venda.merge(vendas, on="venda_id")
base = base[base["status"] == "concluida"].copy()
base["faturamento"] = base["quantidade"] * base["preco_unitario"] - base["desconto"]
base["data_venda"] = pd.to_datetime(base["data_venda"])
base["mes"] = base["data_venda"].dt.strftime("%Y-%m")
mensal = base.groupby("mes", as_index=False)["faturamento"].sum().round(2)
print(mensal)
melhor = mensal.sort_values("faturamento", ascending=False).iloc[0]
print(f"Melhor mês: {melhor['mes']} com R$ {melhor['faturamento']:.2f}")
'''
'''
#4
base = itens_venda.merge(vendas, on="venda_id")
base = base[base["status"] == "concluida"].copy()
base["faturamento"] = base["quantidade"] * base["preco_unitario"] - base["desconto"]

# Passo 1: total de cada venda
total_venda = base.groupby(["venda_id", "unidade_id"], as_index=False)["faturamento"].sum()

# Passo 2: média dos totais por unidade
ticket = total_venda.groupby("unidade_id", as_index=False)["faturamento"].mean()
ticket = ticket.rename(columns={"faturamento": "ticket_medio"})

# Passo 3: nome da unidade
nomes = unidades[["unidade_id", "nome"]].rename(columns={"nome": "unidade"})
ticket = ticket.merge(nomes, on="unidade_id")

print(ticket[["unidade", "ticket_medio"]].round(2).sort_values("ticket_medio", ascending=False))
'''
'''
#5
auditoria = itens_venda.merge(vendas, on="venda_id", how="left", indicator=True)
sem_venda = auditoria[auditoria["_merge"] == "left_only"].copy()

sem_venda["valor"] = (
    sem_venda["quantidade"] * sem_venda["preco_unitario"] - sem_venda["desconto"]
)

nomes = itens[["item_id", "nome"]].rename(columns={"nome": "item"})
sem_venda = sem_venda.merge(nomes, on="item_id")

relatorio = sem_venda[["venda_id", "item", "quantidade", "valor"]].round(2)
print(relatorio)
print(f"Valor total sem origem: R$ {relatorio['valor'].sum():.2f}")

relatorio.to_csv("auditoria_itens.csv", index=False, encoding="utf-8-sig")
'''
