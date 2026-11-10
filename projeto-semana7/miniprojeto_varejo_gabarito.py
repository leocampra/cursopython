"""
Mini-Projeto Avaliativo - Módulo 1 - Semana 07
Visualização de Dados e Business Intelligence [T4]

GABARITO - Análise Exploratória de Dados (AED) da base Varejo

Este script é uma versão de referência para os alunos compararem com o que
fizeram. Ele segue as sprints do enunciado e cobre os 7 critérios da rubrica:

    Sprint 1 - Importação (leitura nativa com csv.DictReader e com pandas)
    Sprint 2 - Diagnóstico e funções de transformação (texto, inteiro, data)
    Sprint 3 - Limpeza de nulos e duplicatas + regra de negócio do CO_ID
    Sprint 4 - Estatística descritiva do número de filhos (CL_FHL)
    Sprint 5 - Agrupamentos, contadores do relatório, conclusões e exportação

Como executar:
    pip install pandas
    python miniprojeto_varejo_gabarito.py
    python miniprojeto_varejo_gabarito.py "caminho/para/Base Varejo.csv"

Sem argumento, o script procura "Base Varejo.csv" na mesma pasta dele.
No Google Colab: envie o CSV e este arquivo e rode
    %run miniprojeto_varejo_gabarito.py "Base Varejo.csv"

Os arquivos gerados vão para a pasta "saidas/".
"""

import csv
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

PASTA = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
SAIDAS = PASTA / "saidas"

# Textos que a base usa no lugar de "vazio". O pandas NÃO reconhece "#N/D"
# como nulo sozinho: para ele, "#N/D" é um texto qualquer.
MARCADORES_AUSENTES = {"", "#N/D", "N/D", "NA", "N/A", "NULL", "NAN"}

COLUNAS_UTEIS = ["DATA", "CO_ID", "CL_ID", "CL_GENERO", "CL_EC", "CL_FHL",
                 "CL_SEG", "PR_ID", "PR_CAT", "PR_NOME"]

# Legenda do estado civil, tirada do PDF que acompanha a base no Kaggle.
ESTADO_CIVIL = {1: "Casado/União estável", 2: "Divorciado", 3: "Separado",
                4: "Solteiro", 5: "Viúvo"}


def titulo(texto):
    """Imprime um cabeçalho para separar as etapas no terminal."""
    print("\n" + "=" * 72)
    print(texto)
    print("=" * 72)


def numero(valor):
    """Formata inteiros no padrão brasileiro (830.000)."""
    return f"{int(valor):,}".replace(",", ".")


def localizar_base():
    """Usa o caminho passado na linha de comando ou procura o CSV na pasta."""
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        caminho = Path(sys.argv[1])
        if caminho.exists():
            return caminho
        sys.exit(f"Arquivo não encontrado: {caminho}")
    for nome in ["Base Varejo.csv", "Varejo.csv", "BaseVarejo.csv"]:
        caminho = PASTA / nome
        if caminho.exists():
            return caminho
    sys.exit("Base não encontrada. Baixe 'Base Varejo.csv' do Kaggle e coloque "
             "na mesma pasta do script, ou passe o caminho como argumento.")


# =========================================================================
# SPRINT 2 - FUNÇÕES DE TRANSFORMAÇÃO (texto, inteiro e data)
# Ficam no topo porque são usadas nas sprints seguintes.
# =========================================================================

def limpar_texto(valor):
    """Padroniza um texto: tira espaços das pontas, junta espaços repetidos
    (expressão regular) e passa para maiúsculas. Marcadores como '#N/D'
    viram None, que é o nulo de verdade."""
    if valor is None or pd.isna(valor):
        return None
    texto = re.sub(r"\s+", " ", str(valor)).strip().upper()
    if texto in MARCADORES_AUSENTES:
        return None
    else:
        return texto


def converter_inteiro(valor):
    """Converte para inteiro aceitando só dígitos (expressão regular).
    Qualquer outra coisa vira None, para ser tratada depois."""
    if valor is None or pd.isna(valor):
        return None
    texto = str(valor).strip()
    if re.fullmatch(r"\d+", texto):
        return int(texto)
    else:
        return None


def converter_data(texto):
    """Converte a string de DATA em datetime usando o módulo datetime.

    ATENÇÃO: esta base mistura dois formatos de data.
      - Quando o 1º número é maior que 12, ele só pode ser o dia: dd/mm/aaaa.
      - Quando o 1º número é até 12, a data está no padrão americano: mm/dd/aaaa.
    A Sprint 2 mostra a evidência disso (a ordem do arquivo e do CO_ID).
    """
    if texto is None or pd.isna(texto):
        return None
    texto = str(texto).strip()
    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", texto):
        return None
    primeiro_numero = int(texto[:2])
    if primeiro_numero > 12:
        formato = "%d/%m/%Y"
    else:
        formato = "%m/%d/%Y"
    try:
        return datetime.strptime(texto, formato)
    except ValueError:
        return None


def aplicar_por_valor_unico(serie, funcao):
    """Aplica a função só uma vez para cada valor diferente e depois espalha o
    resultado. Com 830 mil linhas e poucos valores distintos (1.300 datas, por
    exemplo), isso deixa o script muito mais rápido que um .apply() linha a linha."""
    mapa = {valor: funcao(valor) for valor in serie.dropna().unique()}
    return serie.map(mapa)


def tratar_categoria(valor):
    """Regra da rubrica: categoria vazia vira 'Sem Categoria'."""
    if valor is None or pd.isna(valor):
        return "Sem Categoria"
    else:
        return valor


def tratar_nome_produto(valor):
    """Mesmo raciocínio para o nome do produto."""
    if valor is None or pd.isna(valor):
        return "Produto não identificado"
    else:
        return valor


def estatisticas(serie):
    """Os 7 parâmetros pedidos no enunciado."""
    return {
        "Contagem": int(serie.count()),
        "Média": round(float(serie.mean()), 3),
        "Mediana": float(serie.median()),
        "Desvio padrão": round(float(serie.std()), 3),
        "Moda": ", ".join(str(int(m)) for m in serie.mode()),
        "Máximo": int(serie.max()),
        "Mínimo": int(serie.min()),
    }


def main():
    caminho_base = localizar_base()
    SAIDAS.mkdir(exist_ok=True)

    # =====================================================================
    # SPRINT 1 - IMPORTAÇÃO DOS DADOS
    # =====================================================================
    titulo("SPRINT 1 - IMPORTAÇÃO DOS DADOS")

    # 1a) Leitura nativa e estruturada com csv.DictReader (critério 3).
    # Cada linha vira um dicionário {nome_da_coluna: valor}.
    with open(caminho_base, encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=";")
        primeira_linha = next(leitor)
        total_linhas_nativo = 1 + sum(1 for _ in leitor)
        nomes_colunas = leitor.fieldnames

    print("Leitura com csv.DictReader:")
    print(f"  Registros lidos: {numero(total_linhas_nativo)}")
    print(f"  Cabeçalho: {nomes_colunas}")
    print("  Os 4 nomes vazios no fim vêm do ';;;;' que termina cada linha do arquivo.")
    print(f"  Primeiro registro como dicionário: "
          f"{ {k: v for k, v in primeira_linha.items() if k} }")

    # 1b) Leitura com pandas, que é o que usamos no resto da análise.
    # dtype=str mantém tudo como texto: assim NÓS decidimos como converter
    # cada coluna (Sprint 2), em vez de deixar o pandas adivinhar.
    df_bruto = pd.read_csv(caminho_base, sep=";", encoding="utf-8", dtype=str)
    tipos_inferidos = pd.read_csv(caminho_base, sep=";", encoding="utf-8",
                                  nrows=1000).dtypes

    print("\nLeitura com pandas:")
    print(f"  Número de registros: {numero(df_bruto.shape[0])}")
    print(f"  Número de colunas:   {df_bruto.shape[1]}")
    print(f"  Colunas: {df_bruto.columns.tolist()}")
    print("\n  Tipos que o pandas infere sozinho (amostra de 1.000 linhas):")
    print(tipos_inferidos.to_string())
    print("\n  Observação: DATA chega como texto, não como data.")

    # =====================================================================
    # SPRINT 2 - DIAGNÓSTICO E TRANSFORMAÇÃO DE TIPOS
    # =====================================================================
    titulo("SPRINT 2 - DIAGNÓSTICO DE QUALIDADE")

    # Problema 1: nulos por coluna.
    print("[1] Valores nulos por coluna (o que o pandas enxerga como nulo):")
    print(df_bruto.isna().sum().to_string())

    colunas_vazias = [c for c in df_bruto.columns if df_bruto[c].isna().all()]
    print(f"\n    Colunas 100% vazias: {colunas_vazias}")

    # Problema 2: nulos "disfarçados" de texto.
    print("\n[2] Nulos disfarçados de texto ('#N/D'):")
    disfarcados = {}
    for coluna in COLUNAS_UTEIS:
        qtd = int(df_bruto[coluna].str.strip().str.upper().isin(MARCADORES_AUSENTES).sum())
        if qtd > 0:
            disfarcados[coluna] = qtd
            print(f"    {coluna}: {numero(qtd)}")
    produtos_nd = df_bruto.loc[df_bruto["PR_CAT"] == "#N/D", "PR_ID"].unique().tolist()
    print(f"    Todos pertencem ao(s) PR_ID: {produtos_nd}")

    # Problema 3: duplicatas exatas.
    duplicatas = int(df_bruto.duplicated().sum())
    print(f"\n[3] Linhas duplicadas (iguais em todas as colunas): {numero(duplicatas)} "
          f"({duplicatas / len(df_bruto):.1%} da base)")

    # Problema 4: textos fora do padrão (ex.: minúsculas no meio do nome).
    nomes_fora_padrao = sorted(n for n in df_bruto["PR_NOME"].dropna().unique()
                               if n != n.upper())
    print(f"\n[4] Nomes de produto fora do padrão de maiúsculas: {nomes_fora_padrao}")

    # Problema 5: o mesmo nome de produto com mais de um código.
    nomes_com_varios_ids = (df_bruto.groupby("PR_NOME")["PR_ID"].nunique() > 1).sum()
    print(f"\n[5] Nomes de produto com mais de um PR_ID: {nomes_com_varios_ids} "
          f"(ex.: PRESUNTO COZIDO tem "
          f"{df_bruto.loc[df_bruto['PR_NOME'] == 'PRESUNTO COZIDO', 'PR_ID'].nunique()} códigos)")

    # Problema 6: as datas. Testamos as duas leituras possíveis.
    print("\n[6] Formato da coluna DATA:")
    texto_data = df_bruto["DATA"].str.strip()
    primeiro = texto_data.str[:2].astype(int)
    segundo = texto_data.str[3:5].astype(int)
    print(f"    Datas com o 1º número > 12 (só podem ser dd/mm): {numero((primeiro > 12).sum())}")
    print(f"    Datas com o 2º número > 12 (só podem ser mm/dd): {numero((segundo > 12).sum())}")

    data_ddmm = pd.to_datetime(texto_data, format="%d/%m/%Y", errors="coerce")
    data_correta = aplicar_por_valor_unico(texto_data, converter_data)
    data_correta = pd.to_datetime(data_correta)

    # Evidência: o CO_ID (número da nota) cresce com o tempo. Numa leitura
    # correta, nenhuma compra pode ter data anterior à compra de número menor.
    def compras_fora_de_ordem(datas):
        compras = (pd.DataFrame({"CO_ID": df_bruto["CO_ID"].astype(int), "DATA": datas})
                   .drop_duplicates("CO_ID").sort_values("CO_ID"))
        return int((compras["DATA"].diff().dt.days < 0).sum())

    print(f"    Lendo tudo como dd/mm/aaaa: {numero(data_ddmm.isna().sum())} inválidas, "
          f"{compras_fora_de_ordem(data_ddmm)} compras com data anterior à compra anterior, "
          f"período {data_ddmm.min():%d/%m/%Y} a {data_ddmm.max():%d/%m/%Y}")
    print(f"    Lendo com a regra mista:    {numero(data_correta.isna().sum())} inválidas, "
          f"{compras_fora_de_ordem(data_correta)} compras fora de ordem, "
          f"período {data_correta.min():%d/%m/%Y} a {data_correta.max():%d/%m/%Y}")
    print(f"    O arquivo fica em ordem cronológica com a regra mista? "
          f"{'Sim' if data_correta.is_monotonic_increasing else 'Não'}")
    print("    Conclusão: a base mistura mm/dd/aaaa (1º número até 12) com dd/mm/aaaa.")
    print("    Ler tudo como dd/mm não dá erro nenhum, mas troca o mês de "
          f"{numero((data_ddmm != data_correta).sum())} registros.")

    # ---------------------------------------------------------------------
    # Transformação: aplicamos as funções da Sprint 2 em cada coluna.
    # ---------------------------------------------------------------------
    titulo("SPRINT 2 - TRANSFORMAÇÃO DE TEXTOS, INTEIROS E DATAS")

    df = df_bruto.drop(columns=colunas_vazias).copy()

    for coluna in ["CL_GENERO", "CL_SEG", "PR_CAT", "PR_NOME"]:
        df[coluna] = aplicar_por_valor_unico(df[coluna], limpar_texto)

    for coluna in ["CO_ID", "CL_ID", "CL_EC", "CL_FHL", "PR_ID"]:
        df[coluna] = aplicar_por_valor_unico(df[coluna], converter_inteiro).astype("Int64")

    df["DATA"] = data_correta

    print(f"Colunas vazias removidas: {colunas_vazias}")
    print("Textos padronizados: CL_GENERO, CL_SEG, PR_CAT, PR_NOME ('#N/D' virou nulo de verdade)")
    print("Inteiros convertidos: CO_ID, CL_ID, CL_EC, CL_FHL, PR_ID")
    print("DATA convertida com datetime.strptime e a regra mista de formato")
    print("\nTipos depois da transformação:")
    print(df.dtypes.to_string())
    print("\nNulos depois da transformação:")
    print(df.isna().sum().to_string())

    # =====================================================================
    # SPRINT 3 - LIMPEZA DE NULOS, DUPLICATAS E REGRA DO CO_ID
    # =====================================================================
    titulo("SPRINT 3 - LIMPEZA DE NULOS E DUPLICATAS")

    # 3a) Categoria e nome vazios (critério 4).
    # Decisão: PREENCHER, não apagar. São vendas reais de um produto que só
    # não tem cadastro (PR_ID 107). Apagar reduziria os totais sem motivo.
    nulos_categoria = int(df["PR_CAT"].isna().sum())
    df["PR_CAT"] = df["PR_CAT"].apply(tratar_categoria)
    df["PR_NOME"] = df["PR_NOME"].apply(tratar_nome_produto)
    print(f"[a] {numero(nulos_categoria)} categorias vazias preenchidas com 'Sem Categoria' "
          "e o nome com 'Produto não identificado'.")
    print("    Justificativa: são vendas reais; apagar tiraria itens das contagens.")

    # 3b) Dimensões físicas (critério 4).
    # Esta base NÃO tem peso, altura, largura nem outra medida física.
    # O equivalente aqui são os atributos do cliente. A regra que usamos:
    # se faltar, recupera o valor de outra linha do mesmo cliente; se não
    # houver, deixa nulo. Nunca preenchemos com 0, porque 0 filhos é um
    # valor real e inventá-lo distorceria a estatística.
    atributos_cliente = ["CL_GENERO", "CL_EC", "CL_FHL", "CL_SEG"]
    nulos_cliente = int(df[atributos_cliente].isna().sum().sum())
    for coluna in atributos_cliente:
        if df[coluna].isna().any():
            df[coluna] = df[coluna].fillna(df.groupby("CL_ID")[coluna].transform("first"))
    print(f"\n[b] Dimensões físicas: a base não tem nenhuma. Nos atributos do cliente "
          f"havia {nulos_cliente} nulos.")
    print("    Regra: recuperar do próprio cliente; nunca preencher filhos com 0.")

    # 3c) Duplicatas exatas.
    # Decisão: remover. Como não existe coluna de quantidade, não dá para
    # provar que duas linhas idênticas são duas unidades. Uma alternativa
    # igualmente válida é guardar a repetição numa coluna QTD antes de remover.
    antes = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    print(f"\n[c] Duplicatas removidas: {numero(antes - len(df))}. Restaram {numero(len(df))} linhas.")
    print("    Alternativa aceitável: contar as repetições numa coluna QTD antes de remover.")

    # 3d) Regra de negócio do identificador de compra (critério 5).
    # CO_ID é o número da nota fiscal. Ele se repete porque uma compra tem
    # vários itens. A regra é: cada CO_ID tem UM cliente e UMA data, e o
    # número da nota cresce com o tempo. Registros que quebram a regra são
    # separados num arquivo próprio, em vez de apagados sem deixar rastro.
    titulo("SPRINT 3 - REGRA DE NEGÓCIO DO IDENTIFICADOR DE COMPRA (CO_ID)")

    resumo_compra = df.groupby("CO_ID").agg(
        clientes=("CL_ID", "nunique"),
        datas=("DATA", "nunique"),
        itens=("PR_ID", "size"),
        data=("DATA", "min"),
    ).sort_index()
    resumo_compra["fora_de_ordem"] = resumo_compra["data"] < resumo_compra["data"].cummax()

    compras_invalidas = resumo_compra.index[
        (resumo_compra["clientes"] > 1) | (resumo_compra["datas"] > 1)
        | resumo_compra["fora_de_ordem"]
    ]
    sem_identificador = df["CO_ID"].isna() | df["CL_ID"].isna() | df["DATA"].isna()
    mascara_invalida = sem_identificador | df["CO_ID"].isin(compras_invalidas)

    registros_invalidos = df[mascara_invalida].copy()
    df = df[~mascara_invalida].copy()

    print(f"Compras distintas (CO_ID): {numero(resumo_compra.shape[0])}")
    print(f"Compras com mais de um cliente: {int((resumo_compra['clientes'] > 1).sum())}")
    print(f"Compras com mais de uma data:   {int((resumo_compra['datas'] > 1).sum())}")
    print(f"Compras com data anterior a uma nota de número menor: "
          f"{int(resumo_compra['fora_de_ordem'].sum())}")
    print(f"Linhas sem CO_ID, CL_ID ou DATA válidos: {int(sem_identificador.sum())}")
    print(f"Registros separados em saidas/registros_invalidos.csv: {numero(len(registros_invalidos))}")
    print(f"Itens por compra: média {resumo_compra['itens'].mean():.1f}, "
          f"de {resumo_compra['itens'].min()} a {resumo_compra['itens'].max()}")

    # Cadastro do cliente: o mesmo CL_ID deve ter sempre os mesmos atributos.
    variacao = df.groupby("CL_ID")[atributos_cliente].nunique()
    print(f"Clientes com cadastro que muda entre linhas: {int((variacao > 1).any(axis=1).sum())}")

    # Colunas auxiliares para as análises.
    df["ANO"] = df["DATA"].dt.year
    df["ANO_MES"] = df["DATA"].dt.to_period("M").astype(str)
    df["ESTADO_CIVIL"] = df["CL_EC"].map(ESTADO_CIVIL)

    # =====================================================================
    # SPRINT 4 - ESTATÍSTICA DESCRITIVA DO NÚMERO DE FILHOS (CL_FHL)
    # =====================================================================
    titulo("SPRINT 4 - ESTATÍSTICA DESCRITIVA: NÚMERO DE FILHOS (CL_FHL)")

    # CL_FHL é um dado do CLIENTE, mas aparece repetido em cada item que ele
    # compra. Se calcularmos na tabela inteira, quem compra mais pesa mais.
    # Por isso a estatística principal usa UMA linha por cliente.
    clientes = df.drop_duplicates("CL_ID")[["CL_ID", "CL_GENERO", "CL_SEG",
                                            "ESTADO_CIVIL", "CL_FHL"]]
    est_clientes = estatisticas(clientes["CL_FHL"])
    est_linhas = estatisticas(df["CL_FHL"])

    print(f"{'Parâmetro':<15}{'Por cliente':>14}{'Por linha (comparação)':>26}")
    for parametro in est_clientes:
        print(f"{parametro:<15}{str(est_clientes[parametro]):>14}"
              f"{str(est_linhas[parametro]):>26}")

    sem_filhos = int((clientes["CL_FHL"] == 0).sum())
    print(f"\nClientes sem filhos: {sem_filhos} de {len(clientes)} "
          f"({sem_filhos / len(clientes):.1%})")
    print("Distribuição (clientes por número de filhos):")
    print(clientes["CL_FHL"].value_counts().sort_index().to_string())

    # =====================================================================
    # SPRINT 5 - AGRUPAMENTOS
    # Base sem preço: "vendas" aqui = itens (linhas) e "compras" = CO_ID distintos.
    # =====================================================================
    titulo("SPRINT 5 - PADRÕES DE AGRUPAMENTO")

    # Agrupamento 1: gênero.
    por_genero = df.groupby("CL_GENERO").agg(
        clientes=("CL_ID", "nunique"),
        compras=("CO_ID", "nunique"),
        itens=("PR_ID", "size"),
    )
    por_genero["itens_por_compra"] = (por_genero["itens"] / por_genero["compras"]).round(1)
    por_genero["compras_por_cliente"] = (por_genero["compras"] / por_genero["clientes"]).round(1)
    print("[1] Quem compra mais? (por gênero)")
    print(por_genero.to_string())

    # Agrupamento 2: categoria.
    por_categoria = df.groupby("PR_CAT").agg(
        itens=("PR_ID", "size"),
        compras_com_a_categoria=("CO_ID", "nunique"),
        produtos=("PR_ID", "nunique"),
    ).sort_values("itens", ascending=False)
    por_categoria["%_itens"] = (por_categoria["itens"] / len(df) * 100).round(1)
    print("\n[2] Quais categorias vendem mais? (itens por categoria)")
    print(por_categoria.to_string())

    # Agrupamento 3: pivot_table categoria x gênero, em % dentro de cada gênero.
    pivot_genero = pd.pivot_table(df, index="PR_CAT", columns="CL_GENERO",
                                  values="PR_ID", aggfunc="count", fill_value=0)
    pivot_genero_pct = (pivot_genero / pivot_genero.sum() * 100).round(1)
    print("\n[3] pivot_table: % dos itens de cada gênero em cada categoria")
    print(pivot_genero_pct.to_string())

    # Agrupamento 4: segmento econômico.
    por_segmento = df.groupby("CL_SEG").agg(
        clientes=("CL_ID", "nunique"),
        compras=("CO_ID", "nunique"),
        itens=("PR_ID", "size"),
    ).sort_index()
    por_segmento["itens_por_compra"] = (por_segmento["itens"] / por_segmento["compras"]).round(1)
    print("\n[4] Por segmento econômico")
    print(por_segmento.to_string())

    # Agrupamento 5: tempo (só faz sentido com as datas convertidas certo).
    por_ano = df.groupby("ANO").agg(compras=("CO_ID", "nunique"), itens=("PR_ID", "size"),
                                    meses_com_venda=("ANO_MES", "nunique"))
    print("\n[5] Como as vendas variam ao longo do tempo? (por ano)")
    print(por_ano.to_string())

    por_mes = df.groupby("ANO_MES")["CO_ID"].nunique()
    print(f"\n    Compras por mês: média {por_mes.mean():.0f}, "
          f"menor {por_mes.min()} ({por_mes.idxmin()}), maior {por_mes.max()} ({por_mes.idxmax()})")
    print(f"    Primeiro mês: {por_mes.index[0]} ({por_mes.iloc[0]} compras) | "
          f"último mês: {por_mes.index[-1]} ({por_mes.iloc[-1]} compras)")

    # Agrupamento 6: filhos x categoria (pivot_table em %).
    pivot_filhos = pd.pivot_table(df, index="CL_FHL", columns="PR_CAT", values="PR_ID",
                                  aggfunc="count", fill_value=0)
    pivot_filhos_pct = (pivot_filhos.div(pivot_filhos.sum(axis=1), axis=0) * 100).round(1)
    print("\n[6] pivot_table: % de cada categoria no carrinho, por número de filhos")
    print(pivot_filhos_pct.to_string())

    # =====================================================================
    # SPRINT 5 - RELATÓRIO FINAL (contadores) E CONCLUSÕES
    # =====================================================================
    titulo("SPRINT 5 - RELATÓRIO FINAL")

    contadores = {
        "Registros na base original": numero(len(df_bruto)),
        "Colunas na base original": df_bruto.shape[1],
        "Colunas vazias removidas": len(colunas_vazias),
        "Duplicatas removidas": numero(duplicatas),
        "Categorias '#N/D' tratadas (após duplicatas)": numero(
            int((df["PR_CAT"] == "Sem Categoria").sum())),
        "Registros separados pela regra do CO_ID": numero(len(registros_invalidos)),
        "Registros na base limpa": numero(len(df)),
        "Clientes distintos": numero(df["CL_ID"].nunique()),
        "Compras distintas (CO_ID)": numero(df["CO_ID"].nunique()),
        "Produtos distintos (PR_ID)": numero(df["PR_ID"].nunique()),
        "Período": f"{df['DATA'].min():%d/%m/%Y} a {df['DATA'].max():%d/%m/%Y}",
    }
    for nome, valor in contadores.items():
        print(f"  {nome:<46}: {valor}")

    genero_top = por_genero["compras"].idxmax()
    cat_top = por_categoria.index[0]
    tres_maiores = por_categoria["%_itens"].iloc[:3].sum()

    print("\nCONCLUSÕES")
    print(f"1. {cat_top} concentra {por_categoria['%_itens'].iloc[0]}% dos itens; "
          f"as 3 maiores categorias somam {tres_maiores:.1f}%.")
    print(f"2. O gênero {genero_top} faz mais compras "
          f"({numero(por_genero.loc[genero_top, 'compras'])}), mas tem mais clientes; "
          f"o mix de categorias é praticamente igual entre os gêneros.")
    print(f"3. {sem_filhos / len(clientes):.1%} dos clientes não têm filhos: mediana e moda "
          f"são 0 e a média é {est_clientes['Média']}.")
    print(f"4. Cada compra tem em média {resumo_compra['itens'].mean():.1f} itens; "
          f"o segmento B reúne {por_segmento.loc['B', 'clientes'] / len(clientes):.1%} dos clientes.")
    print("5. A base mistura dois formatos de data; lida errado, distorce qualquer análise "
          "mensal ou sazonal.")
    print("6. Problemas que permanecem: sem preço nem quantidade, produto 107 sem cadastro "
          f"e {nomes_com_varios_ids} nomes de produto com mais de um código.")

    # Exportação (carga do ETL).
    df.to_csv(SAIDAS / "df_limpo.csv", sep=";", index=False, encoding="utf-8-sig",
              date_format="%Y-%m-%d")
    registros_invalidos.to_csv(SAIDAS / "registros_invalidos.csv", sep=";", index=False,
                               encoding="utf-8-sig", date_format="%Y-%m-%d")
    print(f"\nArquivos gravados em {SAIDAS.name}/: df_limpo.csv, registros_invalidos.csv")


if __name__ == "__main__":
    main()
