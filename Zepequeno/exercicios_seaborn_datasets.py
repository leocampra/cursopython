"""Aula: Visualização com Seaborn com os datasets dos slides

Datasets de exemplo do Seaborn: flights, penguins, iris, titanic, tips, exercise

Estes são os exercícios dos slides da semana 12. Eles servem para aprender a
sintaxe com dados simples. Depois de cada um, faça o exercício de mesmo número
com a base da Zé Pequeno (Zepequeno/exercicios_seaborn.py).

    Pergunta -> Dados -> Tipo de gráfico -> Ajustes -> Interpretação

Como fazer: escreva o código onde está "# Seu código aqui" e responda às
perguntas nas linhas "# Resposta:". Os valores em "Confira" servem para você
saber se acertou. Os exemplos resolvidos já desenham o gráfico.

Os datasets são baixados da internet na primeira vez que sns.load_dataset()
roda. Depois ficam guardados no computador.

ATENÇÃO ao copiar código do PDF: o "fl" de "flights" e o "fi" de "figuras"
vêm como um caractere só (ligadura) e o código dá erro. Digite os nomes.

Bibliotecas:
    pip install pandas matplotlib seaborn
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 30)
pd.set_option("display.float_format", "{:,.2f}".format)

voos = sns.load_dataset("flights")        # passageiros por mês, 1949 a 1960
pinguins = sns.load_dataset("penguins")   # medidas de 344 pinguins de 3 espécies
iris = sns.load_dataset("iris")           # medidas de 150 flores de 3 espécies
titanic = sns.load_dataset("titanic")     # 891 passageiros do Titanic
gorjetas = sns.load_dataset("tips")       # 244 contas de um restaurante
exercicio = sns.load_dataset("exercise")  # pulsação de 30 pessoas em 3 momentos

sns.set_theme(style="whitegrid")

pasta_graficos = Path(__file__).parent / "graficos_seaborn" / "datasets"
pasta_graficos.mkdir(parents=True, exist_ok=True)

def mostrar_grafico(nome_arquivo):
    """Salva o gráfico atual em graficos_seaborn/datasets e exibe na tela."""
    plt.tight_layout()
    plt.savefig(pasta_graficos / nome_arquivo, dpi=110, bbox_inches="tight")
    plt.show()
    plt.close("all")

# #####################################################################
# AULA 1 — GRÁFICOS BÁSICOS: LINHA, BARRA E DISPERSÃO (slide 21)
# #####################################################################

# =====================================================================
# EXERCÍCIO 1 — Gráfico de linha (flights)
# Pergunta: como o número de passageiros mudou ao longo dos anos?
# =====================================================================

# a) Linha de passageiros por ano (exemplo resolvido)

print(voos.head())
plt.figure(figsize=(9, 4))
sns.lineplot(data=voos, x="year", y="passengers", marker="o")
plt.title("Passageiros por ano")
plt.xlabel("Ano")
plt.ylabel("Passageiros (milhares)")
mostrar_grafico("ex1a_voos_linha.png")

# Resposta: cada ano tem 12 linhas na tabela (uma por mês). O que o ponto de
#           cada ano representa? E a faixa sombreada em volta da linha?

# b) Refaça mostrando o TOTAL de passageiros do ano, sem a faixa sombreada.
#    Dica: estimator="sum" e errorbar=None
#    Confira: 1949 = 1.520 | 1960 = 5.714
plt.figure(figsize=(9, 4))
sns.lineplot(data=voos, x="year", y="passengers", estimator="sum", errorbar=None, marker="o" color="#ffffff")
plt.title("Total de passageiros por ano")
plt.xlabel("Ano")
plt.ylabel("Passageiros (milhares)")
mostrar_grafico("ex1b_voos_total.png")
total_ano = voos.groupby("year")["passengers"].sum()
print(f"Total 1949: {total_ano[1949]:,} | 1960: {total_ano[1960]:,}")

# c) Faça uma linha por mês (hue="month"). Use palette="flare" e coloque a
#    legenda fora do gráfico: plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
#    Confira: o mês com mais passageiros em média é Jul.
plt.figure(figsize=(10, 5))
sns.lineplot(data=voos, x="year", y="passengers", hue="month", palette="dark")
plt.title("Passageiros por ano, uma linha por mês")
plt.xlabel("Ano")
plt.ylabel("Passageiros (milhares)")
plt.legend(title="Mês", bbox_to_anchor=(1.01, 1), loc="upper left")
mostrar_grafico("ex1c_voos_mes.png")
pico = voos.groupby("month", observed=True)["passengers"].mean().idxmax()
print("Mês com mais passageiros em média:", pico)

# Resposta: além do crescimento, que padrão se repete todo ano?

# =====================================================================
# EXERCÍCIO 2 — Gráfico de barra (penguins)
# Pergunta: qual espécie de pinguim tem maior massa corporal?
# =====================================================================

# a) Faça um barplot da massa corporal (body_mass_g) por espécie (species),
#    com título e rótulos.
#    Confira: Adelie 3.700,66 | Chinstrap 3.733,09 | Gentoo 5.076,02
plt.figure(figsize=(7, 4))
sns.barplot(data=pinguins, x="species", y="body_mass_g")
plt.title("Massa corporal média por espécie")
plt.xlabel("Espécie")
plt.ylabel("Massa corporal (g)")
mostrar_grafico("ex2a_pinguins_barra.png")
print(pinguins.groupby("species")["body_mass_g"].mean())

# Resposta: qual espécie é a mais pesada? A barra mostra a soma ou a média?
#           O que é o traço preto no topo de cada barra?

# b) Separe por sexo com hue="sex" e tire o traço preto (errorbar=None).
#    Confira: Gentoo macho 5.484,84 g
plt.figure(figsize=(7, 4))
sns.barplot(data=pinguins, x="species", y="body_mass_g", hue="sex", errorbar=None)
plt.title("Massa corporal média por espécie e sexo")
plt.xlabel("Espécie")
plt.ylabel("Massa corporal (g)")
mostrar_grafico("ex2b_pinguins_sexo.png")
print(pinguins.groupby(["species", "sex"])["body_mass_g"].mean())

# Resposta: o macho é mais pesado em todas as espécies?

# c) Quantos pinguins de cada espécie há em cada ilha? Use sns.countplot com
#    x="island" e hue="species".
#    Confira: Biscoe 168 | Dream 124 | Torgersen 52
ordem = pinguins["island"].value_counts().index
plt.figure(figsize=(7, 4))
sns.countplot(data=pinguins, x="island", hue="species", order=ordem)
plt.title("Quantidade de pinguins por ilha e espécie")
plt.xlabel("Ilha")
plt.ylabel("Quantidade")
mostrar_grafico("ex2c_pinguins_ilha.png")
print(pd.crosstab(pinguins["island"], pinguins["species"]))

# Resposta: por que o countplot não precisa de y? Alguma espécie vive em uma
#           ilha só?

# =====================================================================
# EXERCÍCIO 3 — Gráfico de dispersão (penguins)
# Pergunta: existe relação entre o comprimento da nadadeira e a massa corporal?
# =====================================================================

# a) Dispersão do comprimento da nadadeira (flipper_length_mm, eixo x) e da
#    massa corporal (body_mass_g, eixo y). Calcule a correlação.
#    Dica: pinguins["flipper_length_mm"].corr(pinguins["body_mass_g"])
#    Confira: 0,87
plt.figure(figsize=(7, 5))
sns.scatterplot(data=pinguins, x="flipper_length_mm", y="body_mass_g")
plt.title("Comprimento da nadadeira x massa corporal")
plt.xlabel("Nadadeira (mm)")
plt.ylabel("Massa corporal (g)")
mostrar_grafico("ex3a_pinguins_dispersao.png")
r = pinguins["flipper_length_mm"].corr(pinguins["body_mass_g"])
print(f"Correlação nadadeira x massa: {r:.2f}")

# Resposta: existe relação? Ela é positiva ou negativa, forte ou fraca?

# b) Repita com hue="species" e size="bill_length_mm" (slide 20). Calcule a
#    correlação dentro de cada espécie.
#    Dica: for especie, grupo in pinguins.groupby("species"): ...
#    Confira: Adelie 0,47 | Chinstrap 0,64 | Gentoo 0,70
plt.figure(figsize=(8, 5))
sns.scatterplot(data=pinguins, x="flipper_length_mm", y="body_mass_g", hue="species", 
                size="bill_length_mm", alpha=0.7)
plt.title("Nadadeira x massa por espécie (tamanho = bico)")
plt.xlabel("Nadadeira (mm)")
plt.ylabel("Massa corporal (g)")
plt.legend(bbox_to_anchor=(1.01, 1), loc="upper left")
mostrar_grafico("ex3b_pinguins_especie.png")
for especie, grupo in pinguins.groupby("species"):
    print(f"{especie}: {grupo['flipper_length_mm'].corr(grupo['body_mass_g']):.2f}")

# Resposta: por que a correlação dentro de cada espécie é menor que a do total?


# #####################################################################
# AULA 2 — CORRELAÇÃO, HEATMAPS E CUSTOMIZAÇÃO
# #####################################################################

# =====================================================================
# EXERCÍCIO 4 — Heatmap de correlação (tips, iris, titanic)
# Pergunta: quais variáveis andam juntas?
# =====================================================================

# a) Tips (slide 24, exemplo resolvido)
'''
corr_gorjetas = gorjetas.corr(numeric_only=True)
print(corr_gorjetas)
plt.figure(figsize=(5, 4))
sns.heatmap(corr_gorjetas, annot=True, cmap="coolwarm", center=0, linewidths=0.5)
plt.title("Matriz de correlação — Tips")
plt.tight_layout()
plt.show()
'''
# Resposta: conta e gorjeta andam juntas (0,68). Isso quer dizer que uma
#           CAUSA a outra?

# b) Iris (slide 28). Rode a linha abaixo e veja o erro. Depois corrija,
#    calcule a matriz de correlação e faça o heatmap com annot=True e
#    cmap="viridis". Em seguida, refaça com cmap="coolwarm", center=0,
#    vmin=-1, vmax=1.
#    Confira: petal_length x petal_width 0,96 | sepal_width x petal_length -0,43
# iris.corr()   # <- tire o # para ver o erro
# Seu código aqui

# Resposta: por que o .corr() deu erro?
# Resposta: em qual das duas paletas dá para ver que -0,43 é negativo?

# c) Titanic (slide 29): quais variáveis têm maior correlação com "survived"?
#    Primeiro rode as linhas abaixo e veja quantas linhas sobram com dropna():
print("Linhas:", len(titanic))
print("Linhas depois de titanic.dropna():", len(titanic.dropna()))
print(titanic.isnull().sum())
#    Agora selecione só as colunas ["survived", "pclass", "age", "sibsp",
#    "parch", "fare"], faça o dropna() DEPOIS, calcule a correlação e faça
#    dois heatmaps lado a lado: um com "coolwarm" e outro com "rocket".
#    Dica: fig, axes = plt.subplots(1, 2, figsize=(13, 5)) e ax=axes[0] / ax=axes[1]
#    Confira: 714 linhas | pclass -0,36 | fare 0,27
# Seu código aqui

# Resposta: por que o dropna() na tabela inteira deixou só 182 linhas?
# Resposta: qual variável é a mais correlacionada com survived? O que o sinal
#           negativo quer dizer na prática?

# d) O heatmap só usa colunas numéricas. Crie a coluna mulher (1 ou 0) e
#    calcule a correlação dela com survived. Calcule também a taxa de
#    sobrevivência por sexo.
#    Dica: titanic["mulher"] = (titanic["sex"] == "female").astype(int)
#          titanic.groupby("sex")["survived"].mean()
#    Confira: correlação 0,54 | female 0,74 | male 0,19
# Seu código aqui

# Resposta: qual era a variável mais importante e por que ela não apareceu no
#           heatmap do item c?

# =====================================================================
# EXERCÍCIO 5 — Heatmap de tabela (flights)
# Pergunta: dá para ver 12 anos de voos numa figura só?
# =====================================================================

# Monte uma tabela com os meses nas linhas e os anos nas colunas e faça o
# heatmap com annot=True, fmt=".0f" e cmap="flare".
# Dica: tabela_voos = voos.pivot_table(index="month", columns="year",
#                                      values="passengers", observed=True)
# Confira: maior 622 (jul/1960) | menor 104 (nov/1949)
# Seu código aqui

# Resposta: onde aparece o crescimento? E a sazonalidade?
# Resposta: por que aqui a paleta é sequencial e não divergente?

# =====================================================================
# EXERCÍCIO 6 — Customização (tips, slide 38)
# Pergunta: o gráfico conta a história sozinho?
# =====================================================================

# a) Barplot de total_bill por day, com o tema whitegrid, a paleta "flare",
#    título e rótulos nos eixos.
#    Rode primeiro com palette="flare" sem hue e leia o aviso que aparece.
#    Depois corrija com hue="day" e legend=False.
#    Confira: domingo (Sun) 21,41 é a maior média | sexta (Fri) 17,15 a menor
# Seu código aqui

# Resposta: o que o aviso pede?

# b) Repita o gráfico do item a para cada contexto e compare.
#    Dica: for contexto in ["paper", "notebook", "talk", "poster"]:
#              sns.set_context(contexto) ...
#    No fim, volte ao padrão: sns.set_context("notebook")
# Seu código aqui

# Resposta: o que muda de um contexto para o outro? Qual usar no projetor?

# c) Acrescente ao gráfico do item a uma linha tracejada na média geral
#    (plt.axhline) e uma anotação apontando para a sexta-feira com o número de
#    contas desse dia. Troque o título por uma frase com a conclusão.
#    Dica: (gorjetas["day"] == "Fri").sum()
#          plt.annotate("texto", xy=(1, 17.4), xytext=(0.2, 24),
#                       arrowprops={"arrowstyle": "->", "color": "#333333"})
#    Confira: sexta tem 19 contas
# Seu código aqui

# Resposta: por que é importante avisar o leitor sobre a sexta-feira?

# =====================================================================
# EXERCÍCIO 7 — FacetGrid (exercise, slide 39)
# Pergunta: como a pulsação muda por dieta e tipo de exercício?
# =====================================================================

# Crie uma grade com row="diet" e col="kind", com gráfico de linha de
# x="time" e y="pulse". Personalize os títulos e os eixos.
# Dica: g = sns.FacetGrid(exercicio, row="diet", col="kind")
#       g.map(sns.lineplot, "time", "pulse", marker="o")
#       g.set_titles("Dieta: {row_name} | Atividade: {col_name}")
#       g.set_axis_labels("Tempo", "Pulsação (bpm)")
# Confira: corrida (running) com dieta "no fat" aos 30 min = 140,6
print(exercicio.head())
# Seu código aqui

# Resposta: em qual atividade a pulsação mais sobe? A dieta faz diferença?
# Resposta: as colunas "Unnamed: 0" e "id" servem para a análise?


# #####################################################################
# AULA 3 — SUBPLOTS, LAYOUTS E EXPORTAÇÃO
# #####################################################################

# =====================================================================
# EXERCÍCIO 8 — Subplots e pairplot (tips e penguins, slides 44 e 45)
# Pergunta: como mostrar várias visões numa figura só?
# =====================================================================

# a) Tips em 1 linha x 2 colunas: histograma de total_bill à esquerda e
#    boxplot de total_bill por day à direita (slide 44). Um título para cada
#    gráfico e um título geral.
#    Dica: fig, axes = plt.subplots(1, 2, figsize=(12, 5))
#          sns.histplot(..., ax=axes[0]) | axes[0].set_title(...)
#          fig.suptitle("...")
# Seu código aqui

# Resposta: o que acontece se você usar plt.title("...") depois dos dois
#           gráficos? Teste.

# b) Grade 2 x 2 com os 4 tipos de gráfico da semana, cada um com um dataset:
#      axes[0, 0] -> linha: passageiros por ano (voos, estimator="sum")
#      axes[0, 1] -> barra: massa por espécie (pinguins)
#      axes[1, 0] -> dispersão: total_bill x tip (gorjetas, hue="time")
#      axes[1, 1] -> heatmap: correlação do tips
# Seu código aqui

# c) Pairplot dos pinguins com hue="species" e corner=True (slide 45).
# Seu código aqui

# Resposta: quantas variáveis numéricas entraram? O que aparece na diagonal?
#           Qual espécie se separa das outras?

# =====================================================================
# EXERCÍCIO 9 — Exportação (penguins, slides 46 e 47)
# Pergunta: como entregar o gráfico pronto para o relatório?
# =====================================================================

pasta_figuras = Path(__file__).parent / "figuras"
pasta_figuras.mkdir(exist_ok=True)

# a) Faça a dispersão nadadeira x massa por espécie com
#    fig, ax = plt.subplots(figsize=(8, 5)) e exporte em PNG (dpi=300) e em
#    SVG, os dois com bbox_inches="tight".
#    Dica: fig.savefig(pasta_figuras / "pinguins_nadadeira_massa.png", dpi=300, bbox_inches="tight")
# Seu código aqui

# Resposta: qual a diferença entre PNG e SVG? Quando usar cada um?

# b) Exporte um histograma da massa corporal para CADA espécie, com nomes
#    descritivos: massa_adelie.png, massa_chinstrap.png, massa_gentoo.png
#    Dica: for especie in pinguins["species"].unique(): ...
#          f"massa_{especie.lower()}.png"
#          no fim de cada volta: plt.close(fig)
#    Confira: 3 arquivos novos na pasta figuras.
# Seu código aqui

# Resposta: por que o savefig tem que vir ANTES do plt.show()?
