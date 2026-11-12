"""Aula: SQL avançado — Views (CREATE VIEW)

Banco: zepequeno_dw.sqlite (modelo estrela da Zé Pequeno)

Uma view é uma consulta que ganha um nome e fica salva dentro do banco.
Depois de criada, você consulta a view como se fosse uma tabela:

    CREATE VIEW nome_da_view AS
    SELECT ...

    SELECT * FROM nome_da_view

A view não guarda dados: toda vez que você consulta a view, o banco roda de
novo o SELECT que está dentro dela. Por isso ela sempre mostra os dados
atuais das tabelas.

Para que serve: escrever os JOINs e cálculos uma vez só e reaproveitar em
várias análises, sem copiar e colar a mesma consulta.

Uma regra do SQLite: não dá para criar duas views com o mesmo nome. Por isso,
antes de cada CREATE VIEW, usamos DROP VIEW IF EXISTS. Assim você pode rodar
o arquivo quantas vezes quiser.

    fato_vendas  -> venda_sk, tempo_id, produto_sk, canal_sk, regional_sk,
                    valor_venda, comissao, margem_estimada
    fato_metas   -> tempo_id, regional_sk, valor_meta
    dim_produto  -> produto_sk, nome, categoria
    dim_regional -> regional_sk, nome, tipo, uf, macrorregiao
    dim_tempo    -> tempo_id, ano, mes, nome_mes
    dim_canal    -> canal_sk, nome

Como fazer: escreva o SQL dentro das aspas triplas e tire o # das linhas
logo abaixo (executar e print) para rodar. Faça os exercícios em ordem: cada
view nova usa as views dos exercícios anteriores.
"""
from pathlib import Path
import sqlite3

import pandas as pd

# Troque pelo caminho do banco no seu computador
caminho_banco = Path("/home/leonardo/leoteste/cursopython/Zepequeno/zepequeno_dw.sqlite")

if not caminho_banco.exists():
    raise FileNotFoundError(f"Banco não encontrado: {caminho_banco}")

conexao = sqlite3.connect(caminho_banco)


def executar(sql):
    """Roda comandos que alteram o banco (DROP VIEW, CREATE VIEW) e salva."""
    conexao.executescript(sql)
    conexao.commit()


# ---------------------------------------------------------------------
# EXERCÍCIO 1 — A primeira view: vendas com os nomes
# ---------------------------------------------------------------------
# a) Criar a view vw_vendas_completas (exemplo resolvido)
# Ela junta a fato_vendas com as quatro dimensões. A partir de agora,
# ninguém precisa repetir esses JOINs: basta consultar a view.
sql_1a = """
DROP VIEW IF EXISTS vw_vendas_completas;

CREATE VIEW vw_vendas_completas AS
SELECT f.venda_sk,
       f.tempo_id,
       t.ano,
       t.mes,
       t.nome_mes,
       p.nome         AS produto,
       p.categoria,
       c.nome         AS canal,
       r.nome         AS regional,
       r.tipo         AS tipo_regional,
       r.uf,
       r.macrorregiao,
       f.valor_venda,
       f.comissao,
       f.margem_estimada
FROM fato_vendas AS f
JOIN dim_tempo    AS t ON f.tempo_id = t.tempo_id
JOIN dim_produto  AS p ON f.produto_sk = p.produto_sk
JOIN dim_canal    AS c ON f.canal_sk = c.canal_sk
JOIN dim_regional AS r ON f.regional_sk = r.regional_sk;
"""
executar(sql_1a)
print(pd.read_sql_query("SELECT * FROM vw_vendas_completas LIMIT 5", conexao))

# b) Usar a view: faturamento por regional
# Consulte a view vw_vendas_completas (sem nenhum JOIN!) e mostre, para
# cada regional: regional, qtd_vendas (COUNT) e faturamento (soma de
# valor_venda, arredondada com ROUND(..., 2)), do maior faturamento para o
# menor.
#
# Confira: 11 linhas. Joinville em primeiro, com 254 vendas e 539695,47.
# Curitiba em último, com 3 vendas e 5350,00.
sql_1b = """

"""
# print(pd.read_sql_query(sql_1b, conexao))

# ---------------------------------------------------------------------
# EXERCÍCIO 2 — View de faturamento por mês
# ---------------------------------------------------------------------
# Crie a view vw_faturamento_mensal com uma linha por mês e as colunas:
# tempo_id, ano, nome_mes, qtd_vendas e faturamento (arredondado em 2 casas).
#
# Use a view vw_vendas_completas no FROM: uma view pode ser feita a partir
# de outra view. Não esqueça do GROUP BY com tempo_id, ano e nome_mes.
#
# Siga o modelo do exercício 1a: primeiro o DROP VIEW IF EXISTS, depois o
# CREATE VIEW ... AS SELECT ...
#
# Depois de criar, rode a consulta de conferência, que mostra só 2025.
#
# Confira: Janeiro de 2025 tem 11 vendas e 21150,00. Outubro de 2025 é o
# melhor mês do ano, com 22 vendas e 45280,00.
sql_2 = """

"""
# executar(sql_2)
# print(pd.read_sql_query(
#     "SELECT * FROM vw_faturamento_mensal WHERE ano = 2025 ORDER BY tempo_id",
#     conexao,
# ))

# Para pensar: a dim_tempo tem 60 meses (2022 a 2026), mas a view
# vw_faturamento_mensal tem só 48 linhas. Rode a consulta abaixo e explique
# por que faltam 12 meses.
# print(pd.read_sql_query("SELECT COUNT(*) AS meses FROM vw_faturamento_mensal", conexao))

# ---------------------------------------------------------------------
# EXERCÍCIO 3 — View de resumo por canal de venda
# ---------------------------------------------------------------------
# Crie a view vw_resumo_canal com uma linha por canal e as colunas:
#
#   canal        -> nome do canal
#   qtd_vendas   -> quantidade de vendas
#   faturamento  -> soma de valor_venda
#   comissao     -> soma de comissao
#   margem       -> soma de margem_estimada
#   margem_pct   -> margem dividida pelo faturamento, vezes 100
#
# Arredonde as somas e a porcentagem com ROUND(..., 2). Na porcentagem,
# use 100.0 (com ponto) para o SQLite não fazer conta de número inteiro:
#
#   ROUND(SUM(margem_estimada) * 100.0 / SUM(valor_venda), 2) AS margem_pct
#
# Confira:
#
#   canal        qtd_vendas   faturamento   comissao    margem   margem_pct
#   E-commerce          350     711943,57   85433,24  233725,41       32,83
#   Loja Física         366     765982,50   26809,38  317174,73       41,41
#
# Para pensar: o e-commerce fatura quase o mesmo que a loja física. Por que
# a margem dele é tão menor?
sql_3 = """

"""
# executar(sql_3)
# print(pd.read_sql_query("SELECT * FROM vw_resumo_canal", conexao))

# ---------------------------------------------------------------------
# EXERCÍCIO 4 — Meta x realizado (view em cima de view)
# ---------------------------------------------------------------------
# A gerência quer saber, mês a mês, se cada regional bateu a meta.
# As metas estão na fato_metas e as vendas na vw_vendas_completas.
# Vamos resolver em duas views, um passo de cada vez.
#
# a) Crie a view vw_realizado_regional_mes com as colunas tempo_id,
#    regional e realizado (soma de valor_venda), agrupando por tempo_id e
#    regional. Use a vw_vendas_completas no FROM.
#
# Confira: em Janeiro de 2025 (tempo_id = 202501), Joinville realizou
# 7895,00.
sql_4a = """

"""
# executar(sql_4a)
# print(pd.read_sql_query(
#     "SELECT * FROM vw_realizado_regional_mes WHERE tempo_id = 202501",
#     conexao,
# ))

# b) Complete a view vw_meta_x_realizado trocando cada ______.
# Ela junta as metas com a view do item a. Use LEFT JOIN na view
# vw_realizado_regional_mes: assim os meses com meta e sem nenhuma venda
# continuam aparecendo, com realizado igual a 0. O COALESCE troca o vazio
# (NULL) por 0.
#
# Confira: 177 linhas (o mesmo número de linhas da fato_metas). Em Fevereiro
# de 2025, Florianópolis atingiu 220,10% da meta e Joinville só 20,27%.
sql_4b = """
DROP VIEW IF EXISTS vw_meta_x_realizado;

CREATE VIEW vw_meta_x_realizado AS
SELECT m.tempo_id,
       r.nome                  AS regional,
       m.valor_meta            AS meta,
       COALESCE(v.realizado, 0) AS realizado,
       ROUND(COALESCE(v.realizado, 0) * 100.0 / ______, 2) AS atingimento_pct
FROM fato_metas AS m
JOIN dim_regional AS r ON m.regional_sk = r.regional_sk
______ vw_realizado_regional_mes AS v
       ON v.tempo_id = m.tempo_id
      AND v.regional = ______;
"""
# executar(sql_4b)
# print(pd.read_sql_query(
#     "SELECT * FROM vw_meta_x_realizado WHERE tempo_id BETWEEN 202501 AND 202503 "
#     "ORDER BY tempo_id, regional",
#     conexao,
# ))

# Para pensar: troque o LEFT JOIN por JOIN, rode o item b de novo e conte
# as linhas da view. Quantas sumiram? Que meses são esses? (Depois volte
# para LEFT JOIN e rode mais uma vez.)

# ---------------------------------------------------------------------
# EXERCÍCIO 5 — Analisar a partir das views
# ---------------------------------------------------------------------
# Com as views prontas, a análise fica curta. Consulte só a view
# vw_meta_x_realizado (sem JOIN) e responda: quantos meses cada regional
# bateu a meta (atingimento_pct maior ou igual a 100)?
#
# Mostre regional e meses_meta_batida, do maior para o menor.
#
# Confira: Joinville 24, Blumenau 23 e Florianópolis 23.
sql_5 = """

"""
# print(pd.read_sql_query(sql_5, conexao))

# Desafio: na mesma consulta, acrescente a coluna total_meses (COUNT(*)) e
# a coluna pct_meses_batidos. Dica: dentro do SUM, use CASE WHEN
# atingimento_pct >= 100 THEN 1 ELSE 0 END para contar só os meses batidos.

# ---------------------------------------------------------------------
# EXERCÍCIO 6 — Gerenciar as views (exemplos resolvidos)
# ---------------------------------------------------------------------
# a) Listar as views que existem no banco
# O SQLite guarda a lista de tabelas e views na tabela sqlite_master.
sql_6a = """
SELECT name AS view
FROM sqlite_master
WHERE type = 'view'
ORDER BY name
"""
# print(pd.read_sql_query(sql_6a, conexao))

# b) A view não guarda dados
# Vamos inserir uma venda de teste de 10000,00 em Dezembro de 2025, olhar a
# vw_faturamento_mensal e depois desfazer tudo com rollback(). Nada fica
# gravado no banco. Rode e compare o faturamento de Dezembro antes e
# depois: a view mudou sozinha, sem precisar ser criada de novo.
consulta_dezembro = """
SELECT nome_mes, qtd_vendas, faturamento
FROM vw_faturamento_mensal
WHERE tempo_id = 202512
"""
# print("Antes:")
# print(pd.read_sql_query(consulta_dezembro, conexao))
# conexao.execute("""
#     INSERT INTO fato_vendas (tempo_id, produto_sk, canal_sk, regional_sk,
#                              linha_planilha, valor_venda, quantidade_estimada,
#                              custo_estimado, comissao, margem_estimada)
#     VALUES (202512, 1, 1, 1, 999999, 10000, 0, 0, 0, 0)
# """)
# print("Depois da venda de teste:")
# print(pd.read_sql_query(consulta_dezembro, conexao))
# conexao.rollback()  # desfaz a venda de teste
# print("Depois do rollback:")
# print(pd.read_sql_query(consulta_dezembro, conexao))

# c) Apagar uma view
# DROP VIEW apaga só a view (a consulta salva), nunca os dados das tabelas.
# executar("DROP VIEW IF EXISTS vw_resumo_canal")
# print(pd.read_sql_query(sql_6a, conexao))

# Para pensar: o que acontece se você apagar a vw_vendas_completas e depois
# consultar a vw_faturamento_mensal? Teste e depois rode o exercício 1a
# para criar a view de novo.

conexao.close()
