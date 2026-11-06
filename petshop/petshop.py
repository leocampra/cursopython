from pathlib import Path
import sqlite3

import pandas as pd

# Troque pelo caminho do banco no seu computador
caminho_banco = Path("/home/leonardo/leoteste/petshop.sqlite")

if not caminho_banco.exists():
    raise FileNotFoundError(f"Banco não encontrado: {caminho_banco}")

conexao = sqlite3.connect(caminho_banco)
print("Conectado ao banco!")
'''
clientes = pd.read_sql_query("SELECT * FROM clientes", conexao)
print(clientes.head(3))
print(clientes.shape)
'''

sql = """
SELECT c.nome AS cliente, v.data_venda, v.status 
FROM vendas AS v 
JOIN clientes AS c ON v.cliente_id = c.cliente_id 
WHERE v.forma_pagamento = 'Dinheiro' 
ORDER BY v.data_venda
"""

vendas_dinheiro = pd.read_sql_query(sql, conexao)

print(vendas_dinheiro)

conexao.close()