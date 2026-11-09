"""Aula: SQL avançado — Subconsultas e CTEs (WITH)

Banco: zepequeno_dw.sqlite (modelo estrela da Zé Pequeno)

    fato_vendas  -> uma linha por venda: valor_venda, produto_sk, regional_sk, tempo_id, canal_sk
    dim_produto  -> produto_sk, nome, categoria
    dim_regional -> regional_sk, nome, tipo, uf, macrorregiao
    dim_tempo    -> tempo_id, ano, mes, nome_mes
    dim_canal    -> canal_sk, nome

Como fazer: escreva cada consulta dentro das aspas triplas e tire o # da linha
do print logo abaixo para executar.
"""
from pathlib import Path
import sqlite3

import pandas as pd

# Troque pelo caminho do banco no seu computador
caminho_banco = Path("/home/leonardo/leoteste/cursopython/Zepequeno/zepequeno_dw.sqlite")

if not caminho_banco.exists():
    raise FileNotFoundError(f"Banco não encontrado: {caminho_banco}")

conexao = sqlite3.connect(caminho_banco)

# ---------------------------------------------------------------------
# EXERCÍCIO 1 — Vendas acima da média geral (subconsulta)
# ---------------------------------------------------------------------
# Liste as vendas cujo valor_venda é maior que a média de valor_venda de
# todas as vendas. Mostre: venda_sk, ano, nome_mes, produto, regional e
# valor_venda, da maior venda para a menor.
#
# Regra: a média deve ser calculada pela própria consulta, com uma
# subconsulta no WHERE. Não digite o número da média no código.
#
# Dica: comece escrevendo só a consulta que calcula a média e rode.
#
# Confira: a média geral é 2064,14, o resultado tem 360 linhas e a maior
# venda vale 2991,00.

sql_1 = """
-- escreva sua consulta aqui
"""
# print(pd.read_sql_query(sql_1, conexao))

# ---------------------------------------------------------------------
# EXERCÍCIO 2 — Contagem por estado, cidade e região (CTE)
# ---------------------------------------------------------------------
# A CTE vendas_acima abaixo já está pronta. Ela funciona como uma tabela
# temporária com as vendas acima da média geral e as colunas cidade, tipo,
# uf e macrorregiao. Você só precisa escrever o SELECT que vem depois dela.
#
# Rode o item a, que já está resolvido, e observe como ele conta por estado.
# Depois faça os itens b e c copiando o modelo e trocando o que for preciso.

cte_vendas_acima = """
WITH vendas_acima AS (
    SELECT f.venda_sk,
           r.nome AS cidade,
           r.tipo,
           r.uf,
           r.macrorregiao
    FROM fato_vendas AS f
    JOIN dim_regional AS r ON f.regional_sk = r.regional_sk
    WHERE f.valor_venda > (SELECT AVG(valor_venda) FROM fato_vendas)
)
"""

# a) Contagem por estado (exemplo resolvido)
# O WHERE deixa só as cidades, porque as macrorregiões não têm estado (uf = 'N/A').
sql_2a = cte_vendas_acima + """
SELECT uf AS estado, COUNT(*) AS vendas_acima_media
FROM vendas_acima
WHERE tipo = 'Cidade'
GROUP BY uf
ORDER BY vendas_acima_media DESC
"""
print(pd.read_sql_query(sql_2a, conexao))

# b) Contagem por cidade
# Copie o modelo e troque a coluna uf pela coluna cidade.
# Confira: 5 cidades, com Joinville em primeiro (141 vendas).
sql_2b = cte_vendas_acima + """
-- escreva aqui somente o SELECT
"""
# print(pd.read_sql_query(sql_2b, conexao))

# c) Contagem por região
# Copie o modelo, use a coluna macrorregiao e apague o WHERE, porque todas
# as vendas têm região.
# Confira: 5 regiões, com Sul em primeiro (344 vendas).
sql_2c = cte_vendas_acima + """
-- escreva aqui somente o SELECT
"""
# print(pd.read_sql_query(sql_2c, conexao))

# Para pensar: Curitiba tem vendas no banco. Por que ela não aparece no item b?

# ---------------------------------------------------------------------
# EXERCÍCIO 3 — Vendas dos 3 produtos mais vendidos (CTE)
# ---------------------------------------------------------------------
# Crie uma CTE chamada top_produtos com os 3 produtos de maior faturamento
# (soma de valor_venda). Depois, junte essa CTE com as tabelas necessárias e
# retorne as vendas desses produtos: produto, ano, nome_mes, regional e
# valor_venda, ordenando por produto e, dentro dele, da maior venda para a
# menor.
#
# Dica: rode primeiro só o SELECT de dentro da CTE e veja o ranking.
#
# Confira: o resultado tem 716 linhas, sendo 356 de Rolhas e 360 de Paçoca.
#
# Para pensar: você pediu 3 produtos com LIMIT 3. Por que só 2 aparecem?

sql_3 = """
-- escreva sua consulta aqui
"""
# print(pd.read_sql_query(sql_3, conexao))

conexao.close()
