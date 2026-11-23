"""Aula: Visualização com Seaborn com a base da Zé Pequeno

Banco: zepequeno_dw.sqlite (modelo estrela da Zé Pequeno)

Na semana passada usamos gráficos para INVESTIGAR os dados (AED). Agora o foco
é COMUNICAR: escolher o gráfico certo, deixar claro o que ele mostra e
entregar a figura pronta para um relatório.

    Pergunta -> Dados -> Tipo de gráfico -> Ajustes -> Interpretação

    1. Gráfico certo  -> sns.lineplot(), sns.barplot(), sns.scatterplot(), sns.heatmap()
    2. Contexto       -> título com a mensagem, rótulos com unidade, anotações
    3. Estilo         -> sns.set_theme(), paletas, sns.set_context()
    4. Layout         -> plt.subplots(), sns.FacetGrid(), sns.pairplot()
    5. Exportação     -> fig.savefig("arquivo.png", dpi=300, bbox_inches="tight")

Os exemplos dos slides (com os datasets do Seaborn) estão em outro arquivo:
exercicios_seaborn_datasets.py. A numeração é a mesma: o exercício 1 de lá e o
exercício 1 daqui tratam do mesmo assunto.

Tabelas usadas:
    vw_vendas_completas  -> 1 linha = 1 venda (716 vendas)
    dim_tempo            -> calendário com os 60 meses (2022 a 2026)
    vw_meta_x_realizado  -> meta e realizado por regional e mês (177 linhas)

Como fazer: escreva o código onde está "# Seu código aqui" e responda às
perguntas nas linhas "# Resposta:". Os valores em "Confira" servem para você
saber se acertou. Os exemplos resolvidos já desenham o gráfico.

Bibliotecas:
    pip install pandas matplotlib seaborn
"""
from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Troque pelo caminho do banco no seu computador
caminho_banco = Path("/home/leonardo/leoteste/cursopython/Zepequeno/zepequeno_dw.sqlite")

if not caminho_banco.exists():
    raise FileNotFoundError(f"Banco não encontrado: {caminho_banco}")

conexao = sqlite3.connect(caminho_banco)

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", "{:,.2f}".format)

# Vendas: 1 linha = 1 lançamento de venda da planilha
df = pd.read_sql_query("SELECT * FROM vw_vendas_completas", conexao)

# Faturamento mês a mês com o calendário completo (60 meses, 0 nos meses vazios).
# É a mesma tabela que montamos no exercício 3 da AED.
mensal = pd.read_sql_query("SELECT tempo_id, ano, mes, nome_mes FROM dim_tempo", conexao)
faturamento = df.groupby("tempo_id")["valor_venda"].sum()
mensal["faturamento"] = mensal["tempo_id"].map(faturamento).fillna(0)
mensal["periodo"] = pd.to_datetime(mensal["tempo_id"].astype(str), format="%Y%m")

# Metas: 1 linha = 1 regional em 1 mês (só Joinville, Blumenau e Florianópolis)
metas = pd.read_sql_query("SELECT * FROM vw_meta_x_realizado", conexao)
metas["ano"] = metas["tempo_id"] // 100

sns.set_theme(style="whitegrid")


# #####################################################################
# AULA 1 — GRÁFICOS BÁSICOS: LINHA, BARRA E DISPERSÃO
# #####################################################################

# =====================================================================
# EXERCÍCIO 1 — Gráfico de linha: tendência no tempo
# Pergunta: a Zé Pequeno está vendendo mais ao longo dos anos?
# =====================================================================

# a) Valor da venda por ano (exemplo resolvido)
plt.figure(figsize=(9, 4))
sns.lineplot(data=df, x="ano", y="valor_venda", marker="o")
plt.title("Valor da venda por ano")
plt.xlabel("Ano")
plt.ylabel("Valor da venda (R$)")
plt.xticks(range(2022, 2027))
plt.tight_layout()
plt.show()
# Resposta: cada ano tem de 97 a 195 vendas. O que o ponto de cada ano
#           representa: a soma ou a média? E a faixa sombreada?

#    Refaça mostrando o FATURAMENTO TOTAL de cada ano, sem a faixa sombreada.
#    Dica: estimator="sum" e errorbar=None
#    Confira: 2022 221.780,50 | 2024 405.457,00 (maior) | 2026 196.500,57
# Seu código aqui

# Resposta: os dois gráficos contam a mesma história? A queda de 2026 é real?

# b) Mês a mês: rode o jeito ERRADO (exemplo resolvido)
plt.figure(figsize=(11, 4))
sns.lineplot(data=df, x="tempo_id", y="valor_venda")
plt.title("ERRADO: tempo_id como número e média por venda")
plt.tight_layout()
plt.show()
# Resposta: aponte 3 problemas deste gráfico.
#   Dica: o que acontece entre 202212 e 202301 no eixo x? O lineplot está
#   somando ou fazendo média? Os meses sem venda aparecem?

# c) Agora faça certo: use a tabela "mensal" (x="periodo", y="faturamento"),
#    com marker="o", título e rótulos.
#    Confira: 60 meses; maior mês 202306 com R$ 55.522,00; 12 meses com zero.
# Seu código aqui


# d) Faça uma linha por ano: tabela mensal, x="mes", y="faturamento", hue="ano",
#    palette="deep". Dica: plt.xticks(range(1, 13)) mostra os 12 meses.
# Seu código aqui

# Resposta: os anos têm o mesmo "patamar"? O que acontece em 2023 e 2026?

# =====================================================================
# EXERCÍCIO 2 — Gráfico de barra: comparar categorias
# Pergunta: qual produto, canal e regional vende mais?
# =====================================================================

# a) Faça um barplot do valor_venda por produto, com título e rótulos.
#    Confira: Paçoca 1.987,59 | Rolhas 2.141,56
# Seu código aqui

# Resposta: qual produto tem a venda maior? A barra mostra a soma ou a média?
#           O que é o traço preto no topo de cada barra?

# b) Separe por canal com hue="canal" e tire o traço preto (errorbar=None).
#    Confira: Paçoca/E-commerce 1.944,25 | Rolhas/Loja Física 2.159,73
# Seu código aqui

# Resposta: em qual canal a venda é maior, nos dois produtos?

# c) Rode o barplot por regional abaixo (exemplo resolvido).
ordem_qtd = df["regional"].value_counts().index
plt.figure(figsize=(11, 4))
sns.barplot(data=df, x="regional", y="valor_venda", order=ordem_qtd, errorbar=None)
plt.xticks(rotation=45)
plt.title("Valor por regional")
plt.tight_layout()
plt.show()
# Resposta: pelo gráfico, qual regional parece a "melhor"? Quantas vendas ela tem?

#    Refaça com estimator="sum", ordenando as barras pelo faturamento total.
#    Dica: total_reg = df.groupby("regional")["valor_venda"].sum().sort_values(ascending=False)
#          order=total_reg.index
#    Confira: Joinville 539.695,47 | Florianópolis 438.976,80 | Blumenau 427.186,80
# Seu código aqui

# Resposta: qual dos dois gráficos responde "onde a Zé Pequeno vende mais?"
#           O que o barplot calcula quando você não informa o estimator?

# d) Faturamento por produto (x) e canal (hue), com estimator="sum" e errorbar=None.
#    Confira: Rolhas/Loja Física 388.750,90 (maior) | Paçoca/E-commerce 338.299,37 (menor)
# Seu código aqui

# Resposta: algum canal domina? Onde está a maior diferença?

# =====================================================================
# EXERCÍCIO 3 — Gráfico de dispersão: relação entre duas variáveis
# Pergunta: quando uma variável aumenta, a outra muda junto?
# =====================================================================

# a) Dispersão da meta (x) e do realizado (y), usando a tabela metas.
#    Calcule a correlação e conte quantas linhas têm realizado igual a zero.
#    Dica: metas["meta"].corr(metas["realizado"])
#    Confira: correlação 0,02 | 39 linhas com zero
# Seu código aqui

# Resposta: o que é a fileira de pontos deitada lá embaixo? Uma correlação de
#           0,02 quer dizer que a meta não tem nada a ver com o realizado?

# b) Repita só com os meses que tiveram venda, com hue="regional".
#    Calcule a correlação geral e a de cada regional.
#    Dica: com_venda = metas[metas["realizado"] > 0]
#          for regional, grupo in com_venda.groupby("regional"): ...
#    Confira: 0,74 | Blumenau 0,83 | Florianópolis 0,74 | Joinville 0,62
# Seu código aqui

# Resposta: o que mudou na conclusão? O que isso ensina sobre dado faltante?

# c) Dispersão de valor_venda (x) e comissao (y), com hue="canal".
#    Calcule a correlação total e a de cada canal, e o % médio da comissão
#    (comissao / valor_venda) em cada canal.
#    Confira: total 0,32 | cada canal 1,00 | E-commerce 12,0 % | Loja Física 3,5 %
# Seu código aqui

# Resposta: o que são as duas "retas"? Uma correlação de 0,32 quer dizer que a
#           comissão é "quase aleatória"?


# #####################################################################
# AULA 2 — CORRELAÇÃO, HEATMAPS E CUSTOMIZAÇÃO
# #####################################################################

# =====================================================================
# EXERCÍCIO 4 — Heatmap de correlação
# Pergunta: quais variáveis andam juntas?
# =====================================================================

# a) Rode a linha abaixo e veja o erro. Depois corrija com numeric_only=True e
#    faça o heatmap com annot=True, fmt=".2f" e cmap="viridis".
# df.corr()   # <- tire o # para ver o erro
# Seu código aqui

# Resposta: por que o .corr() deu erro?
# Resposta: o heatmap mostra tempo_id x ano = 1,00 e venda_sk x ano = -0,43.
#           Essas correlações dizem algo sobre o negócio? Por quê?

#    Agora faça o heatmap só com valor_venda, comissao e margem_estimada,
#    usando cmap="coolwarm", center=0, vmin=-1, vmax=1.
#    Confira: valor x margem 0,87 | valor x comissão 0,32 | comissão x margem -0,16
# Seu código aqui

# Resposta: em qual das duas paletas dá para ver que -0,16 é negativo?

# b) Metas: faça dois heatmaps lado a lado com meta, realizado e
#    atingimento_pct: um com todas as linhas e outro só com os meses com venda.
#    Dica: fig, axes = plt.subplots(1, 2, figsize=(13, 5)) e ax=axes[0] / ax=axes[1]
#          com_venda = metas[metas["realizado"] > 0]
#    Confira: meta x realizado 0,02 com zeros e 0,74 sem | 138 linhas sem zeros
# Seu código aqui

# Resposta: os 39 zeros são vendas reais? O que acontece com a matriz se você
#           não tratar o dado faltante antes de calcular?

# c) O heatmap só usa colunas numéricas. Crie a coluna ecommerce (1 ou 0) e
#    refaça o heatmap com valor_venda, comissao, margem_estimada e ecommerce.
#    Calcule também a margem média por canal.
#    Dica: df["ecommerce"] = (df["canal"] == "E-commerce").astype(int)
#    Confira: ecommerce x comissão 0,90 | ecommerce x margem -0,50
#             margem média: E-commerce 667,79 | Loja Física 866,60
# Seu código aqui

# Resposta: qual variável mais explica a comissão e a margem? Por que ela não
#           apareceu no heatmap do item a?

# d) Faça o heatmap de valor_venda, comissao e margem_estimada separado por
#    canal (dois heatmaps lado a lado).
#    Confira: valor x comissão 1,00 nos dois canais
# Seu código aqui

# Resposta: compare com o 0,32 do item a. O que o heatmap do total esconde?

# =====================================================================
# EXERCÍCIO 5 — Heatmap além da correlação: tabelas coloridas
# Pergunta: dá para ver 5 anos de vendas numa figura só?
# =====================================================================

# a) Faturamento por ano (linhas) e mês (colunas), em R$ mil (exemplo resolvido).
tabela = df.pivot_table(index="ano", columns="mes", values="valor_venda", aggfunc="sum") / 1000
print(tabela)
plt.figure(figsize=(12, 4))
sns.heatmap(tabela, annot=True, fmt=".1f", cmap="flare", linewidths=0.5,
            cbar_kws={"label": "Faturamento (R$ mil)"})
plt.title("Faturamento por ano e mês (R$ mil)")
plt.xlabel("Mês")
plt.ylabel("Ano")
plt.tight_layout()
plt.show()
#    Confira: 12 células vazias | maior célula 55,5 (jun/2023)
# Resposta: o que são as células em branco? E os dois valores quase brancos
#           (1,5 e 2,3) no meio delas? Já vimos isso na AED?

# b) Faça o mesmo heatmap com a QUANTIDADE de vendas.
#    Dica: contagem = pd.crosstab(df["ano"], df["mes"])
#          sns.heatmap(..., annot=True, fmt="d", cmap="Blues")
# Seu código aqui

# Resposta: no crosstab os buracos viram 0; no pivot_table viram vazio.
#           "Zero" e "vazio" querem dizer a mesma coisa?

# c) Atingimento médio da meta por regional (linhas) e ano (colunas), só com
#    os meses com venda. Use uma paleta divergente centrada em 100.
#    Dica: atingimento = com_venda.pivot_table(index="regional", columns="ano",
#                                              values="atingimento_pct", aggfunc="mean")
#          sns.heatmap(atingimento, annot=True, fmt=".0f", cmap="vlag", center=100)
#          plt.yticks(rotation=0)
#    Confira: 2025 acima de 100 nas 3 regionais (Joinville 119,5) | Joinville 2026 85,6
# Seu código aqui

# Resposta: por que nos itens a e b a paleta é sequencial e aqui é divergente?
# Resposta: 2025 ficou todo vermelho. Foi um ano excelente? (lembre da AED)

# =====================================================================
# EXERCÍCIO 6 — Customização: estilo, paleta, contexto e anotações
# Pergunta: o gráfico conta a história sozinho?
# =====================================================================

fat_ano = df.groupby("ano")["valor_venda"].sum().reset_index()
fat_ano["faturamento_mil"] = fat_ano["valor_venda"] / 1000

# a) Barplot de faturamento_mil por ano (tabela fat_ano), com o tema
#    whitegrid, a paleta "flare", título e rótulos nos eixos.
#    Rode primeiro com palette="flare" sem hue e leia o aviso que aparece.
#    Depois corrija com hue="ano" e legend=False.
#    Confira: 2024 é o maior ano (405,46 mil)
# Seu código aqui

# Resposta: o que o aviso pede?

# b) Repita o gráfico do item a para cada contexto e compare.
#    Dica: for contexto in ["paper", "notebook", "talk", "poster"]:
#              sns.set_context(contexto) ...
#    No fim, volte ao padrão: sns.set_context("notebook")
# Seu código aqui

# Resposta: o que muda de um contexto para o outro? Qual usar no projetor?

# c) "Antes e depois". Faturamento por mês nos anos completos (2022, 2024 e
#    2025). O ANTES já está pronto:
anos_completos = df[df["ano"].isin([2022, 2024, 2025])]
por_mes = anos_completos.groupby("mes")["valor_venda"].sum()
plt.figure(figsize=(9, 4))
sns.barplot(x=por_mes.index, y=por_mes.values)
plt.tight_layout()
plt.show()
#    Faça o DEPOIS, um gráfico que conte a história sozinho:
#      - título com a CONCLUSÃO (não só o assunto)
#      - eixo y em R$ mil, com a unidade no rótulo
#      - meses com nome (Jan, Fev, ...) no eixo x
#      - outubro em destaque e os outros meses em cinza
#      - uma linha tracejada na média: plt.axhline(...)
#      - uma anotação apontando para outubro: plt.annotate(...)
#    Dicas:
#      nomes = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
#      dados = pd.DataFrame({"mes": nomes, "faturamento_mil": por_mes.values / 1000})
#      cores = {nome: ("#2a9d8f" if nome == "Out" else "#c8c8c8") for nome in nomes}
#      sns.barplot(data=dados, x="mes", y="faturamento_mil", hue="mes", palette=cores, legend=False)
#      plt.annotate("texto", xy=(9, 104.8), xytext=(5.6, 108), arrowprops={"arrowstyle": "->"})
#    Confira: outubro 104.822,00 | média mensal 80.642,88 | março 59.998,55 (menor)
# Seu código aqui

# Resposta: mostre os dois gráficos para alguém que não conhece a base. Em qual
#           deles a pessoa entende a mensagem sem você explicar?

# d) Que tipo de paleta (categórica, sequencial ou divergente) você usaria em:
# Resposta: cores para os canais E-commerce e Loja Física?
# Resposta: heatmap de correlação (de -1 a +1)?
# Resposta: heatmap de faturamento ano x mês?
# Resposta: heatmap de atingimento da meta (em volta de 100 %)?

# =====================================================================
# EXERCÍCIO 7 — FacetGrid e relplot: um gráfico por grupo
# Pergunta: o padrão é o mesmo em todos os grupos?
# =====================================================================

# a) Grade com row="produto" e col="canal", com o histograma do valor_venda
#    em cada painel. Personalize os títulos e os eixos.
#    Dica: g = sns.FacetGrid(df, row="produto", col="canal")
#          g.map(sns.histplot, "valor_venda", bins=15)
#          g.set_titles("{row_name} | {col_name}")
#          g.set_axis_labels("Valor da venda (R$)", "Quantidade de vendas")
#    Confira: 174 | 186 | 176 | 180 vendas; mediana de Rolhas/Loja Física 2.223,50
# Seu código aqui

# Resposta: os 4 grupos têm a mesma forma? Os grupos têm tamanhos parecidos?

# b) Um gráfico de linha do faturamento por mês para cada ano.
#    Use a tabela mensal, col="ano" e col_wrap=3.
# Seu código aqui

# Resposta: quais anos estão completos? Por que é bom todos os painéis terem
#           a mesma escala no eixo y?

# c) Com sns.relplot faça a dispersão de valor_venda x comissao, um painel por
#    canal (col="canal") e cor por produto (hue="produto").
# Seu código aqui

# Resposta: o produto muda a comissão?


# #####################################################################
# AULA 3 — SUBPLOTS, LAYOUTS E EXPORTAÇÃO
# #####################################################################

# =====================================================================
# EXERCÍCIO 8 — Subplots e pairplot
# Pergunta: como mostrar várias visões numa figura só?
# =====================================================================

# a) 1 linha x 2 colunas: histograma do valor_venda à esquerda e boxplot do
#    valor_venda por ano à direita. Um título para cada gráfico e um título geral.
#    Dica: fig, axes = plt.subplots(1, 2, figsize=(12, 5))
#          sns.histplot(..., ax=axes[0]) | axes[0].set_title(...)
#          fig.suptitle("...")
# Seu código aqui

# Resposta: o que acontece se você usar plt.title("...") depois dos dois
#           gráficos? Teste.
# Resposta: o valor típico da venda muda muito de um ano para o outro?

# b) Dois boxplots do valor_venda lado a lado, um por produto e outro por
#    canal, com sharey=True.
#    Confira: mediana Paçoca 1.939,45 | Rolhas 2.190,00
#             mediana E-commerce 2.019,00 | Loja Física 2.103,50
# Seu código aqui

# Resposta: para que serve o sharey=True? O valor da venda muda mais entre
#           produtos ou entre canais?

# c) Pairplot das colunas valor_venda, comissao, margem_estimada com hue="canal".
#    Dica: sns.pairplot(df[["valor_venda", "comissao", "margem_estimada", "canal"]], hue="canal")
# Seu código aqui

# Resposta: quantos painéis aparecem? Que achados da AED da semana passada
#           aparecem neste único gráfico?

# d) Pairplot da tabela metas com meta, realizado, atingimento_pct,
#    hue="regional" e corner=True.
# Seu código aqui

# Resposta: onde aparecem os 39 zeros? Para que serve o corner=True?

# =====================================================================
# EXERCÍCIO 9 — Exportação
# Pergunta: como entregar o gráfico pronto para o relatório?
# =====================================================================

# a) Crie a pasta figuras ao lado deste arquivo (exemplo resolvido).
pasta_figuras = Path(__file__).parent / "figuras"
pasta_figuras.mkdir(exist_ok=True)

# b) Faça o gráfico de faturamento por regional (exercício 2c) com
#    fig, ax = plt.subplots(figsize=(10, 5)) e exporte em PNG (dpi=300) e em
#    SVG, os dois com bbox_inches="tight". Depois mostre o tamanho dos arquivos.
#    Dica: fig.savefig(pasta_figuras / "faturamento_por_regional.png", dpi=300, bbox_inches="tight")
#          for arquivo in pasta_figuras.glob("faturamento_por_regional.*"):
#              print(arquivo.name, arquivo.stat().st_size / 1024, "KB")
# Seu código aqui

# Resposta: abra os dois arquivos e dê zoom. Qual a diferença entre PNG e SVG?
#           Quando usar cada um?

# c) Teste: faça um gráfico qualquer, chame plt.show() e SÓ DEPOIS
#    plt.savefig("teste.png"). Abra o arquivo.
# Seu código aqui

# Resposta: o que saiu no arquivo? Por quê? Qual a regra?

# d) Exporte um gráfico de linha do faturamento mensal para CADA ano, com
#    nomes descritivos: faturamento_mensal_2022.png, faturamento_mensal_2023.png...
#    Dica: for ano in sorted(mensal["ano"].unique()): ...
#          no fim de cada volta: plt.close(fig)
#    Confira: 5 arquivos novos na pasta figuras.
# Seu código aqui

# Resposta: para que serve o plt.close(fig) dentro do laço?

# =====================================================================
# DESAFIO — Dashboard executivo da Zé Pequeno (slide 48)
# =====================================================================
# Monte um painel com fig, axes = plt.subplots(2, 2, figsize=(16, 10)):
#   axes[0, 0] -> linha temporal do faturamento mensal (tabela mensal)
#   axes[0, 1] -> heatmap do faturamento por ano e mês (exercício 5)
#   axes[1, 0] -> boxplot do valor da venda por produto e canal
#   axes[1, 1] -> dispersão valor_venda x comissao por canal
# Requisitos:
#   - tema, paleta e contexto iguais em todos os gráficos
#   - cada gráfico com um título que diz a CONCLUSÃO
#   - pelo menos uma anotação (ax.annotate)
#   - título geral (fig.suptitle) e fig.tight_layout()
#   - exportar em PNG (300 dpi) e SVG: figuras/dashboard_zepequeno.png
# Por fim, escreva 3 frases para o dono da Zé Pequeno: o que o painel mostra
# e o que ele deveria fazer. Não use termos técnicos sem explicar.
# Seu código aqui


conexao.close()
