"""Aula: Análise Exploratória de Dados (AED) com a base da Zé Pequeno

Banco: zepequeno_dw.sqlite (modelo estrela da Zé Pequeno)

AED é investigar os dados ANTES de tirar conclusões: entender a estrutura,
medir, desenhar e desconfiar. Cada exercício parte de uma pergunta de negócio.

    1. Carregar   -> pd.read_sql_query(...)
    2. Explorar   -> df.shape, df.head(), df.info(), df.describe()
    3. Verificar  -> df.isnull().sum(), df.duplicated().sum()
    4. Visualizar -> sns.histplot(), sns.boxplot(), sns.scatterplot()
    5. Concluir   -> escreva o que achou, em português, nos comentários

Como fazer: escreva o código onde está "# Seu código aqui" e responda às
perguntas nas linhas "# Resposta:". Os valores em "Confira" servem para você
saber se acertou. Os exemplos resolvidos já imprimem o resultado.

Bibliotecas:
    pip install matplotlib seaborn
    pip install ydata-profiling sweetviz "setuptools<81"   (só para o exercício 8)

    O ydata-profiling ainda usa pkg_resources, que saiu do setuptools 81. Sem o
    "setuptools<81" o import dá: ModuleNotFoundError: No module named 'pkg_resources'.
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

# A view vw_vendas_completas já junta o fato com as dimensões:
# 1 linha = 1 lançamento de venda da planilha.

df = pd.read_sql_query("SELECT * FROM vw_vendas_completas", conexao)


# 16/11/2026

# =====================================================================
# EXERCÍCIO 1 — Primeiro contato com os dados
# Pergunta: o que tem nesta tabela e de onde vêm as vendas?
# =====================================================================

# a) Formato da tabela (exemplo resolvido)
## print("Formato (linhas, colunas):", df.shape)

# b) Mostre as 5 primeiras linhas e os tipos de cada coluna.
#    Dica: df.head() e df.info()
## print(df.head())
df.info()

# c) Quantos valores diferentes existem nas colunas produto, canal, regional
#    e macrorregiao? Dica: df[[...]].nunique()
#    Confira: produto 2, canal 2, regional 11, macrorregiao 5.
## print(df[["produto", "canal", "regional", "macrorregiao"]].nunique())

# d) Quantas vendas cada regional tem? Dica: value_counts()
#    Confira: Joinville 254, Florianópolis 214, Blumenau 213.
## print(df["regional"].value_counts())
# Resposta: o que chama atenção nas outras 8 regionais?


# e) Algum produto do cadastro (tabela dim_produto) nunca vendeu?
#    Leia dim_produto e use ~produtos["nome"].isin(df["produto"]).
#    Confira: 1 produto.
produtos = pd.read_sql_query("SELECT nome FROM dim_produto", conexao)
nunca_venderam = produtos[~produtos["nome"].isin(df["produto"])]
## print("Produtos sem nenhuma venda:", nunca_venderam["nome"].tolist())
# Resposta: que perguntas você faria ao gestor sobre esse produto?
#['Pé de Moleque'] — está cadastrado e ativo, mas não tem nenhuma venda.
#Pergunta para o negócio: produto novo, erro de cadastro ou vendas perdidas?

# =====================================================================
# EXERCÍCIO 2 — Qualidade: nulos e duplicatas
# Pergunta: posso confiar nesta tabela para calcular médias e totais?
# =====================================================================

# a) Conte os nulos de cada coluna e o total. Confira: total 0.
## print(df.isnull().sum())
## print("Total de nulos:", df.isnull().sum().sum()) 

# b) Conte as linhas inteiras duplicadas. Confira: 0.
## print("Linhas duplicadas:", df.duplicated().sum())

# c) Agora conte as repetições da combinação mês + produto + canal + regional
#    (df.duplicated(subset=chave)) e mostre algumas delas lado a lado
#    (keep=False e sort_values(chave)).
#    Confira: 246 repetições.
chave = ["tempo_id", "produto", "canal", "regional"]
repetidas = df.duplicated(subset=chave).sum()
## print("Repetições de mês+produto+canal+regional:", repetidas)  # 246
## print(df[df.duplicated(subset=chave, keep=False)].sort_values(chave).head(6))
# Pergunta: essas 246 linhas são duplicatas que devem ser removidas? Por quê?
#Resposta: não são duplicatas. A planilha só tem a data do mês (sempre dia 1º),
#então vários lançamentos do mesmo mês caem na mesma combinação. Os valores
#são diferentes. Duplicata se confirma com regra de negócio, não só com código.

# =====================================================================
# EXERCÍCIO 3 — Padrões e anomalias no tempo
# Pergunta: a Zé Pequeno vende de forma regular ao longo dos meses?
# =====================================================================

# a) Monte uma tabela com a quantidade de vendas por ano (linhas) e mês
#    (colunas). Dica: pd.crosstab(df["ano"], df["mes"])
tabela_ano_mes = pd.crosstab(df["ano"], df["mes"])
## print(tabela_ano_mes)
# Resposta: o que acontece no 2º semestre de 2023 e depois de abril de 2026?

# b) Compare com o calendário completo (dim_tempo, 60 meses). O código abaixo
#    junta o calendário com a contagem de vendas e põe 0 nos meses vazios.
tempo = pd.read_sql_query("SELECT tempo_id, ano, mes, nome_mes FROM dim_tempo", conexao)
vendas_por_mes = df.groupby("tempo_id").size().rename("qtd_vendas")
calendario = tempo.merge(vendas_por_mes, on="tempo_id", how="left")
calendario["qtd_vendas"] = calendario["qtd_vendas"].fillna(0).astype(int)
meses_sem_venda = calendario[calendario["qtd_vendas"] == 0]
## print("Meses sem nenhuma venda:", len(meses_sem_venda))         # 12
## print(meses_sem_venda[["tempo_id", "nome_mes"]].to_string(index=False))
# Jul, Ago, Out, Nov e Dez de 2023 e Mai, Jun, Jul, Ago, Out, Nov e Dez de 2026.

#    Filtre os meses com 0 vendas e os meses com só 1 venda. Depois mostre
#    as vendas desses meses de 1 venda (colunas venda_sk, tempo_id, produto,
#    canal, regional, valor_venda).
#    Confira: 12 meses sem venda; 2 meses com 1 venda (202309 e 202609).
meses_com_uma_venda = calendario[calendario["qtd_vendas"] == 1]
## print(meses_com_uma_venda[["tempo_id", "nome_mes", "qtd_vendas"]].to_string(index=False))
# 202309 e 202609: uma única venda isolada no meio de um buraco.
## print(df[df["tempo_id"].isin([202309, 202609])][["venda_sk", "tempo_id", "produto", "canal", "regional", "valor_venda"]])
# Resposta: essas vendas isoladas são confiáveis? O que você faria com elas?
# Anomalia: venda_sk 617 (set/2023) e venda_sk 1 (set/2026). Hipótese: data
# digitada errada. É para investigar na planilha, não para apagar.

# c) Some o valor_venda por mês do ano (groupby("mes")). Qual mês fatura
#    mais e qual fatura menos? Dica: idxmax() e idxmin()
#    Confira: maior = 4 (abril), menor = 9 (setembro).
por_mes = df.groupby("mes")["valor_venda"].sum()
## print(por_mes)
## print("Mês com maior faturamento somado: ", por_mes.idxmax())    # 4 (abril)
## print("Mês com menor faturamento somado: ", por_mes.idxmin())    # 9 (setembro)

#    Repita só com os anos completos (2022, 2024 e 2025) e some por semestre.
#    Dica: anos_completos = df[df["ano"].isin([2022, 2024, 2025])]
#    Confira: 1º semestre 450.425,35 | 2º semestre 517.289,15.
anos_completos = df[df["ano"].isin([2022, 2024, 2025])]
por_mes_completos = anos_completos.groupby("mes")["valor_venda"].sum()
## print(por_mes_completos)
## print("Mês com maior faturamento (anos completos):", por_mes_completos.idxmax())  # 10 (outubro)
semestre = (anos_completos["mes"] > 6).map({False: "1º semestre", True: "2º semestre"})
## print(anos_completos.groupby(semestre)["valor_venda"].sum())
# Resposta: o 2º semestre vende menos mesmo? O que causou a ilusão?
# Somando todos os anos, setembro (77.172,72) fica com 41 % de abril (188.196,50)
# e o 2º semestre parece fraco. Nos anos completos é o contrário: o 2º semestre
# fatura 517.289,15 contra 450.425,35 do 1º, e outubro é o melhor mês.
# A "queda" vinha da falta de dados, não de um padrão real

# d) Gráfico de linha do faturamento mês a mês, com os meses vazios.
#    (exemplo resolvido; rode e descreva o que vê)
faturamento = df.groupby("tempo_id")["valor_venda"].sum()
calendario["faturamento"] = calendario["tempo_id"].map(faturamento).fillna(0)
calendario["periodo"] = pd.to_datetime(calendario["tempo_id"].astype(str), format="%Y%m")
## plt.figure(figsize=(11, 4))
## plt.plot(calendario["periodo"], calendario["faturamento"], marker="o")
## plt.title("Faturamento mensal — Zé Pequeno")
## plt.ylabel("R$")
## plt.tight_layout()
## plt.show()
# Resposta: descreva 3 coisas que o gráfico mostra.

# 18/11/2026

# =====================================================================
# EXERCÍCIO 4 — Estatística descritiva
# Pergunta: quanto vale uma venda "típica" e quanto os valores variam?
# =====================================================================

valor = df["valor_venda"]

# a) Calcule média, mediana, desvio padrão, Q1, Q2, Q3 e IQR (Q3 - Q1)
#    do valor_venda. Dica: valor.quantile([0.25, 0.50, 0.75])
#    Confira: média 2.064,14 | mediana 2.075,50 | desvio 465,75
#             Q1 1.713,25 | Q3 2.430,25 | IQR 717,00
media = valor.mean()
mediana = valor.median()
desvio = valor.std()
q1, q2, q3 = valor.quantile([0.25, 0.50, 0.75])
iqr = q3 - q1
print(f"Média:         {media:,.2f}")     # 2.064,14
print(f"Mediana:       {mediana:,.2f}")   # 2.075,50
print(f"Desvio padrão: {desvio:,.2f}")    # 465,75
print(f"Q1: {q1:,.2f}  Q2: {q2:,.2f}  Q3: {q3:,.2f}")   # 1.713,25 / 2.075,50 / 2.430,25
print(f"IQR:           {iqr:,.2f}")       # 717,00
print(df[["valor_venda", "comissao", "margem_estimada"]].describe())

# b) Calcule o coeficiente de variação (desvio / média x 100) e a assimetria
#    (valor.skew()).
#    Confira: CV 22,6 % | assimetria -0,11
print(f"Coeficiente de variação: {desvio / media * 100:.1f} %")
print(f"Assimetria (skew): {valor.skew():.2f}")
# Resposta: a média representa bem o valor típico aqui? Por quê?
# Média e mediana quase iguais e assimetria perto de zero: distribuição
# simétrica. Aqui a média representa bem o "valor típico" de uma venda.

# c) Repita média, mediana e desvio por produto e por canal.
#    Dica: df.groupby("produto")["valor_venda"].agg(["count", "mean", "median", "std"])
#    Confira: média de Rolhas 2.141,56 | média de Paçoca 1.987,59
print(df.groupby("produto")["valor_venda"].agg(["count", "mean", "median", "std"]))
# Rolhas vende em média R$ 2.141,56 e Paçoca, R$ 1.987,59.
print(df.groupby("canal")["valor_venda"].agg(["count", "mean", "median", "std"]))

# d) Calcule média e mediana da coluna comissao. Depois, por canal.
#    Confira: média 156,76 | mediana 102,55
comissao = df["comissao"]
print(f"Comissão — média {comissao.mean():,.2f} | mediana {comissao.median():,.2f}")
# Resposta: por que média e mediana da comissão ficam tão diferentes?
# 156,76 x 102,55. Média e mediana bem diferentes: a comissão mistura dois grupos
# (3,5 % na Loja Física e 12 % no E-commerce). Nenhuma das duas descreve bem
# "uma comissão típica". O certo é olhar por canal:
print(df.groupby("canal")["comissao"].agg(["mean", "median"]))

# =====================================================================
# EXERCÍCIO 5 — Dados brutos x dados limpos
# Pergunta: o que os valores errados da planilha fazem com as medidas?
# =====================================================================

# a) A tabela auditoria_rejeitados guarda o que o ETL recusou. Na fonte
#    'planilha', o campo registro tem o formato:
#    "data | regional | canal | produto | valor | linha_planilha"
#    O código abaixo separa as partes. Crie a coluna valor_venda (float) com
#    a parte de índice 4 e mostre count, min e max por motivo.
#    Confira: 47 registros; 21 zerados, 18 abaixo e 8 acima da faixa IQR.
rejeitados = pd.read_sql_query(
    "SELECT motivo, registro FROM auditoria_rejeitados WHERE fonte = 'planilha'", conexao
)
partes = rejeitados["registro"].str.split(" | ", regex=False)
rejeitados["valor_venda"] = partes.str[4].astype(float)
print("Registros recusados da planilha:", len(rejeitados))      # 47
print(rejeitados.groupby("motivo")["valor_venda"].agg(["count", "min", "max"]))

# b) Junte os valores limpos com os recusados para recriar a coluna como ela
#    estava na planilha. Dica: pd.concat([...], ignore_index=True)
#    Confira: 763 linhas.
bruto = pd.concat([df["valor_venda"], rejeitados["valor_venda"]], ignore_index=True)
print("Linhas no bruto:", len(bruto)) 

# c) Monte uma tabela comparando count, mean, median, std, min e max do bruto
#    e do limpo. Dica: serie.agg([...]) e pd.DataFrame({"bruto": ..., "limpo": ...})
#    Confira: média bruta 6.619,83 | mediana bruta 2.031,60 | desvio bruto 63.115,61

comparacao = pd.DataFrame({
    "bruto": bruto.agg(["count", "mean", "median", "std", "min", "max"]),
    "limpo": valor.agg(["count", "mean", "median", "std", "min", "max"]),
})
print(comparacao)
# Resposta: qual medida quase não mudou? O que isso ensina?
# Média bruta 6.619,83 x limpa 2.064,14: 8 valores absurdos (99999, 123456,
# 999999) triplicam a média. A mediana quase não muda: 2.031,60 x 2.075,50.
# O desvio padrão vai de 465,75 para 63.115,61. É por isso que a mediana é a
# medida robusta.

# d) Aplique a regra do IQR no bruto, só nos valores positivos (como o ETL fez):
#    limite_inferior = Q1 - 1.5 * IQR e limite_superior = Q3 + 1.5 * IQR.
#    Conte quantos ficam abaixo, acima e quantos são zero.
#    Confira: limites 572,88 a 3.551,88 | abaixo 18 | acima 8 | zerados 21
positivos = bruto[bruto > 0]
b_q1, b_q3 = positivos.quantile([0.25, 0.75])
b_iqr = b_q3 - b_q1
limite_inferior = b_q1 - 1.5 * b_iqr
limite_superior = b_q3 + 1.5 * b_iqr
print(f"Limites IQR do bruto: {limite_inferior:,.2f} a {limite_superior:,.2f}")  # 572,88 a 3.551,88
abaixo = (positivos < limite_inferior).sum()
acima = (positivos > limite_superior).sum()
print("Abaixo:", abaixo, "| Acima:", acima, "| Zerados:", (bruto == 0).sum())   # 18 | 8 | 21

# =====================================================================
# EXERCÍCIO 6 — Visualização para achar padrões e outliers
# Pergunta: o que os gráficos mostram que as tabelas escondem?
# =====================================================================

# a) Histograma do valor_venda com linhas da média e da mediana (exemplo resolvido)
plt.figure(figsize=(8, 4))
sns.histplot(valor, bins=20, kde=True)
plt.axvline(valor.mean(), color="red", linestyle="--", label="média")
plt.axvline(valor.median(), color="green", linestyle=":", label="mediana")
plt.legend()
plt.title("Distribuição do valor da venda (limpo)")
plt.tight_layout()
plt.show()
# Resposta: a distribuição é simétrica, assimétrica, bimodal ou tem outliers?
# Forma: simétrica, média e mediana praticamente no mesmo lugar.

# b) Faça o histograma da comissao (bins=30). Depois refaça com hue="canal".
plt.figure(figsize=(8, 4))
sns.histplot(df["comissao"], bins=30)
plt.title("Comissão — dois picos?")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 4))
sns.histplot(data=df, x="comissao", hue="canal", bins=30)
plt.title("Comissão por canal")
plt.tight_layout()
plt.show()
# Resposta: quantos picos aparecem? O que cada pico representa?
# Bimodal: cada pico é um canal. Subgrupo escondido revelado pelo hue.

# c) Boxplot do bruto (exercício 5) ao lado do boxplot do limpo.
#    Dica: plt.subplot(1, 2, 1) e plt.subplot(1, 2, 2), sns.boxplot(y=...)
plt.figure(figsize=(9, 4))
plt.subplot(1, 2, 1)
sns.boxplot(y=bruto)
plt.title("Bruto (planilha)")
plt.subplot(1, 2, 2)
sns.boxplot(y=valor)
plt.title("Limpo (DW)")
plt.tight_layout()
plt.show()
# Resposta: por que a caixa do bruto fica achatada?
# No bruto a caixa vira uma linha achatada: os 999999 esmagam a escala.

# d) Boxplot do valor_venda por regional, ordenado pela quantidade de vendas.
#    Dica: ordem = df["regional"].value_counts().index
#          sns.boxplot(data=df, x="regional", y="valor_venda", order=ordem)
#          plt.xticks(rotation=45)
ordem = df["regional"].value_counts().index
plt.figure(figsize=(11, 4))
sns.boxplot(data=df, x="regional", y="valor_venda", order=ordem)
plt.xticks(rotation=45)
plt.title("Valor da venda por regional (ordenado pela quantidade de vendas)")
plt.tight_layout()
plt.show()
# Resposta: dá para comparar Joinville com Norte? Por quê?
# As 3 primeiras têm mais de 200 vendas cada. As macrorregiões têm de 3 a 6.
# Caixas com 3 pontos não permitem concluir nada: cuidado com amostras pequenas.

# e) Gráfico de dispersão valor_venda x margem_estimada, com hue="canal".
plt.figure(figsize=(7, 5))
sns.scatterplot(data=df, x="valor_venda", y="margem_estimada", hue="canal", alpha=0.6)
plt.title("Valor da venda x margem estimada")
plt.tight_layout()
plt.show()

# f) Matriz de correlação de valor_venda, comissao e margem_estimada e o
#    heatmap. Dica: df[[...]].corr() e sns.heatmap(..., annot=True)
#    Confira: valor x margem 0,87 | valor x comissão 0,32
correlacao = df[["valor_venda", "comissao", "margem_estimada"]].corr()
print(correlacao)
print("valor x margem:  ", round(correlacao.loc["valor_venda", "margem_estimada"], 2))  # 0,87
print("valor x comissão:", round(correlacao.loc["valor_venda", "comissao"], 2))         # 0,32
plt.figure(figsize=(5, 4))
sns.heatmap(correlacao, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Correlação")
plt.tight_layout()
plt.show()

# Resposta: a correlação de 0,87 é uma descoberta ou vem da fórmula da margem?
#           Por que a comissão quase não acompanha o valor?
# A comissão quase não acompanha o valor porque depende do canal (associação
# com uma variável categórica). E a margem é calculada a partir do valor:
# correlação alta aqui é construção da fórmula, não descoberta.

# 19/11/2026

# =====================================================================
# EXERCÍCIO 7 — Metas: anomalias que o código não pega sozinho
# Pergunta: as regionais estão batendo as metas?
# =====================================================================

metas = pd.read_sql_query("SELECT * FROM vw_meta_x_realizado", conexao)
metas["ano"] = metas["tempo_id"] // 100

# a) Use describe() no atingimento_pct.
#    Confira: média 80,84 | mediana 93,71 | máximo 301,86
# Seu código aqui

# b) Quantas linhas têm realizado igual a zero? Separe por ano. Depois
#    recalcule média e mediana do atingimento sem esses zeros.
#    Confira: 39 linhas (2023: 17 | 2026: 22); sem zeros: média 103,69 | mediana 100,22
# Seu código aqui
# Resposta: esses zeros são regionais que não venderam nada? Compare com o exercício 3.

# c) Quantas linhas passam de 150 % de atingimento? Separe por ano.
#    Confira: 10 linhas (2022: 1 | 2025: 9)
# Seu código aqui

# d) Calcule a meta média por ano e faça um boxplot do atingimento por ano
#    (sem os zeros), com uma linha em 100 %: plt.axhline(100, color="red")
#    Confira: 2022 6.072 | 2023 16.736 | 2024 10.083 | 2025 7.649 | 2026 16.100
# Seu código aqui
# Resposta: 2025 foi um ano excelente? Que hipótese você levaria ao gestor?

# =====================================================================
# EXERCÍCIO 8 — Ferramentas de AED automatizada
# Pergunta: o que a automação encontra sozinha e o que ela deixa passar?
# =====================================================================

# a) Gere o relatório do ydata-profiling e abra o HTML no navegador.
#    from ydata_profiling import ProfileReport
#    perfil = ProfileReport(df, title="AED — Vendas Zé Pequeno", explorative=True)
#    perfil.to_file("relatorio_ydata.html")
# Seu código aqui

# b) Gere o relatório do Sweetviz e a comparação entre os dois canais.
#    import sweetviz as sv
#    relatorio = sv.analyze(df)
#    relatorio.show_html("relatorio_sweetviz.html", open_browser=False)
#    comparacao = sv.compare_intra(df, df["canal"] == "E-commerce", ["E-commerce", "Loja Física"])
#    comparacao.show_html("sweetviz_canais.html", open_browser=False)
# Seu código aqui

# c) Abra os relatórios e responda:
# Resposta: quais alertas aparecem na aba Alerts do ydata-profiling?
# Resposta: algum alerta é "falso" (correlação entre colunas que repetem a
#           mesma informação, ou com um ID)?
# Resposta: os relatórios mostram os meses sem venda (ex. 3) ou as metas
#           baixas de 2025 (ex. 7)? Por quê?

# =====================================================================
# DESAFIO — Relatório de AED
# =====================================================================
# Escreva, em até 10 linhas, os 5 achados mais importantes desta AED para o
# dono da Zé Pequeno. Para cada achado: o que viu, o número que comprova e a
# pergunta ou ação que propõe. Não use termos técnicos sem explicar.

conexao.close()
