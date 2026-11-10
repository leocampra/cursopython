"""Aula: SQL avançado — Window Functions: ROW_NUMBER(), RANK() e SUM() OVER()

Banco: zepequeno_dw.sqlite (modelo estrela da Zé Pequeno)

Uma window function calcula um valor olhando para várias linhas, mas, ao
contrário do GROUP BY, mantém todas as linhas no resultado.

    FUNCAO() OVER (PARTITION BY coluna ORDER BY coluna)

    PARTITION BY -> divide as linhas em grupos (opcional)
    ORDER BY     -> define a ordem dentro de cada grupo

Como fazer: complete as consultas indicadas e tire o # da linha do print logo
abaixo para executar. Os exemplos resolvidos já imprimem o resultado.
"""
from pathlib import Path
import sqlite3

import pandas as pd

# Troque pelo caminho do banco no seu computador
caminho_banco = Path("/home/leonardo/leoteste/cursopython/Zepequeno/zepequeno_dw.sqlite")

if not caminho_banco.exists():
    raise FileNotFoundError(f"Banco não encontrado: {caminho_banco}")

conexao = sqlite3.connect(caminho_banco)

# CTE pronta, usada nos exercícios 1 e 2. Ela já faz os JOINs e entrega as
# colunas venda_sk, produto, ano, nome_mes, regional e valor_venda.
cte_vendas = """
WITH vendas_completas AS (
    SELECT f.venda_sk,
           p.nome AS produto,
           t.ano,
           t.nome_mes,
           r.nome AS regional,
           f.valor_venda
    FROM fato_vendas AS f
    JOIN dim_produto  AS p ON f.produto_sk = p.produto_sk
    JOIN dim_tempo    AS t ON f.tempo_id = t.tempo_id
    JOIN dim_regional AS r ON f.regional_sk = r.regional_sk
)
"""

# ---------------------------------------------------------------------
# EXERCÍCIO 1 — ROW_NUMBER(): numerar as vendas
# ---------------------------------------------------------------------
# a) Numerar todas as vendas, da maior para a menor (exemplo resolvido)
# A coluna venda_sk no ORDER BY desempata vendas de mesmo valor, para a
# numeração sair sempre igual.
sql_1a = cte_vendas + """
SELECT ROW_NUMBER() OVER (ORDER BY valor_venda DESC, venda_sk) AS posicao,
       produto,
       regional,
       valor_venda
FROM vendas_completas
ORDER BY posicao
"""
print(pd.read_sql_query(sql_1a, conexao).head(10))

# b) Numerar as vendas dentro de cada produto
# Copie o modelo e acrescente PARTITION BY produto dentro do OVER, antes do
# ORDER BY, para a numeração recomeçar em cada produto. No ORDER BY final da
# consulta, use produto, posicao.
#
# Confira: 716 linhas. A posição 1 de Paçoca vale 2991,00 e a posição 1 de
# Rolhas vale 2979,00. A última posição de Paçoca é 360 e a de Rolhas é 356.
sql_1b = cte_vendas + """
-- escreva aqui somente o SELECT
"""
# print(pd.read_sql_query(sql_1b, conexao))

# ---------------------------------------------------------------------
# EXERCÍCIO 2 — RANK(): ranking com empates
# ---------------------------------------------------------------------
# ROW_NUMBER() nunca repete um número. RANK() dá a mesma posição para valores
# empatados. Troque o ______ pela função RANK() com um OVER que ordene por
# valor_venda, da maior para a menor. Não use venda_sk aqui: é justamente o
# empate que queremos ver.
#
# Confira, nas vendas de 2960,00 e na venda seguinte:
#
#   valor_venda   numero_linha   ranking
#       2960,00              4         4
#       2960,00              5         4
#       2960,00              6         4
#       2945,00              7         7
#
# Para pensar: por que o ranking pulou de 4 direto para 7?
sql_2 = cte_vendas + """
SELECT regional,
       valor_venda,
       ROW_NUMBER() OVER (ORDER BY valor_venda DESC, venda_sk) AS numero_linha,
       ______ AS ranking
FROM vendas_completas
WHERE produto = 'Paçoca'
ORDER BY numero_linha
"""
# print(pd.read_sql_query(sql_2, conexao).head(10))

# ---------------------------------------------------------------------
# EXERCÍCIO 3 — SUM() OVER(): total e acumulado
# ---------------------------------------------------------------------
# CTE pronta com o faturamento de cada mês de 2025 (uma linha por mês).
cte_meses = """
WITH faturamento_mes AS (
    SELECT t.tempo_id,
           t.nome_mes,
           SUM(f.valor_venda) AS faturamento
    FROM fato_vendas AS f
    JOIN dim_tempo AS t ON f.tempo_id = t.tempo_id
    WHERE t.ano = 2025
    GROUP BY t.tempo_id, t.nome_mes
)
"""

# a) Participação de cada mês no total do ano (exemplo resolvido)
# Com OVER vazio, a soma considera todas as linhas de uma vez.
sql_3a = cte_meses + """
SELECT nome_mes,
       faturamento,
       SUM(faturamento) OVER () AS total_ano,
       ROUND(faturamento * 100.0 / SUM(faturamento) OVER (), 2) AS participacao
FROM faturamento_mes
ORDER BY tempo_id
"""
print(pd.read_sql_query(sql_3a, conexao))

# b) Faturamento acumulado mês a mês
# Mostre nome_mes, faturamento e uma coluna acumulado. Use a mesma soma do
# modelo, mas coloque ORDER BY tempo_id dentro do OVER: assim, cada linha
# soma o próprio mês e todos os anteriores.
#
# Confira: Janeiro acumula 21150,00, Fevereiro acumula 51763,00 e Dezembro
# acumula 340477,00, que é o total do ano.
sql_3b = cte_meses + """
-- escreva aqui somente o SELECT
"""
# print(pd.read_sql_query(sql_3b, conexao))

conexao.close()
