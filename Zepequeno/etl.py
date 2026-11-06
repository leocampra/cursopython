from pathlib import Path
import sqlite3
import pandas as pd

CAMINHO_PLANILHA = "/home/leonardo/leoteste/cursopython/Zepequeno/tabela_vendas_ZePequeno_corrigido.xlsx"
CAMINHO_BRUTO = "/home/leonardo/leoteste/cursopython/Zepequeno/zepequeno_bruto.sqlite"
CAMINHO_DW = "/home/leonardo/leoteste/cursopython/Zepequeno/zepequeno_dw.sqlite"

# ---------------------------------------------------------------------
# Funções de apoio
# ---------------------------------------------------------------------
def criar_chave(coluna):
    """Texto usado só para comparar: 'BLUMENAU ' e 'blumenau' viram o mesmo.

    Evitamos str.title() para corrigir os nomes porque ele estraga alguns
    deles: 'Rio de Janeiro' viraria 'Rio De Janeiro'. O nome oficial vem
    sempre do cadastro no banco bruto.
    """
    return coluna.str.strip().str.casefold()

def texto_para_numero(coluna):
    """Converte 'R$ 92,50', '85,00', '12%' e '96.00' em número."""
    limpa = coluna.str.replace("R$", "", regex=False)
    limpa = limpa.str.replace("%", "", regex=False)
    limpa = limpa.str.replace(",", ".", regex=False)
    return pd.to_numeric(limpa.str.strip())

def texto_para_data(coluna):
    """Converte datas nos dois formatos usados no cadastro de regionais."""
    data_br = pd.to_datetime(coluna, format="%d/%m/%Y", errors="coerce")
    data_iso = pd.to_datetime(coluna, format="%Y-%m-%d", errors="coerce")
    return data_br.fillna(data_iso)

def rejeitar(df, fonte, motivo):
    """Monta as linhas da tabela auditoria_rejeitados."""
    registros = [" | ".join(map(str, linha)) for linha in df.itertuples(index=False)]
    return pd.DataFrame({"registro": registros}).assign(fonte=fonte, motivo=motivo)

# ---------------------------------------------------------------------
# 1. EXTRAÇÃO: lê as fontes sem alterar nada
# ---------------------------------------------------------------------
def extrair():
    for caminho in (CAMINHO_PLANILHA, CAMINHO_BRUTO, CAMINHO_DW):
        if not Path(caminho).exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    brutos = {"vendas": pd.read_excel(CAMINHO_PLANILHA, sheet_name="Vendas_2025")}

    # O número da linha no Excel permite voltar à planilha para conferir.
    # Soma 2 porque o índice começa em 0 e a linha 1 é o cabeçalho.
    brutos["vendas"]["linha_planilha"] = brutos["vendas"].index + 2

    tabelas = ["regionais", "canais", "fornecedores", "produtos",
               "precos_produto", "metas_mensais"]
    conexao = sqlite3.connect(CAMINHO_BRUTO)
    for tabela in tabelas:
        brutos[tabela] = pd.read_sql_query(f"SELECT * FROM {tabela}", conexao)
    conexao.close()

    for nome, df in brutos.items():
        print(f"  {nome:<16} {len(df):>4} linhas")
    return brutos

# ---------------------------------------------------------------------
# 2. TRATAMENTO: uma função para cada tabela do DW
# ---------------------------------------------------------------------
def tratar_regional(brutos):
    regional = brutos["regionais"].copy()
    regional["nome"] = regional["nome"].str.strip()
    regional["uf"] = regional["uf"].str.upper().fillna("N/A")
    regional["gerente"] = regional["gerente"].fillna("Não informado")
    datas = texto_para_data(regional["data_inicio_operacao"])
    regional["data_inicio_operacao"] = datas.dt.strftime("%Y-%m-%d")
    regional["regional_sk"] = range(1, len(regional) + 1)
    return regional

def tratar_canal(brutos):
    canal = brutos["canais"].copy()
    canal["nome"] = canal["nome"].str.strip()
    canal["comissao_pct"] = texto_para_numero(canal["comissao"])
    canal["canal_sk"] = range(1, len(canal) + 1)
    return canal

def tratar_produto(brutos):
    # keep="first": mantém o cadastro original e descarta a repetição.
    produto = brutos["produtos"].drop_duplicates(subset="codigo", keep="first").copy()
    produto["nome"] = produto["nome"].str.strip()

    fornecedores = brutos["fornecedores"].rename(
        columns={"razao_social": "fornecedor", "uf": "fornecedor_uf"}
    )
    produto = produto.merge(
        fornecedores[["fornecedor_id", "fornecedor", "fornecedor_uf"]],
        on="fornecedor_id", how="left",
    )
    produto["produto_sk"] = range(1, len(produto) + 1)
    return produto

def tratar_precos(brutos):
    precos = brutos["precos_produto"].sort_values(["produto_id", "ano"]).copy()
    precos["preco_venda"] = texto_para_numero(precos["preco_venda"])
    precos["custo_unitario"] = texto_para_numero(precos["custo_unitario"])

    # Custo faltando: usa o meio do caminho entre o ano anterior e o seguinte.
    precos["custo_unitario"] = precos.groupby("produto_id")["custo_unitario"].transform(
        lambda custos: custos.interpolate()
    )
    return precos

NOMES_MESES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}

def tratar_tempo(vendas):
    anos = vendas["Data"].dt.year
    meses = pd.date_range(f"{anos.min()}-01-01", f"{anos.max()}-12-01", freq="MS")

    return pd.DataFrame({
        "tempo_id": meses.year * 100 + meses.month,
        "data_inicio": meses.strftime("%Y-%m-%d"),
        "ano": meses.year,
        "semestre": (meses.month - 1) // 6 + 1,
        "trimestre": meses.quarter,
        "mes": meses.month,
        "nome_mes": meses.month.map(NOMES_MESES),
    })

def tratar_vendas(brutos, regional, canal, produto, precos):
    vendas = brutos["vendas"].copy()

    # Valores 0, 99999, 123456 e 999999 são digitação ou preenchimento de
    # sistema. A regra do IQR marca como suspeito o que foge da faixa normal.
    # Ela é calculada sem os zeros para eles não puxarem o limite para baixo.
    positivos = vendas.loc[vendas["Valor_Venda"] > 0, "Valor_Venda"]
    q1 = positivos.quantile(0.25)
    q3 = positivos.quantile(0.75)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    print(f"  Faixa aceita para Valor_Venda: {limite_inferior:.2f} a {limite_superior:.2f}")

    zerado = vendas["Valor_Venda"] <= 0
    baixo = ~zerado & (vendas["Valor_Venda"] < limite_inferior)
    alto = vendas["Valor_Venda"] > limite_superior

    rejeitados = [
        rejeitar(vendas[zerado], "planilha", "Valor zerado"),
        rejeitar(vendas[baixo], "planilha", "Valor abaixo da faixa IQR"),
        rejeitar(vendas[alto], "planilha", "Valor acima da faixa IQR"),
    ]
    vendas = vendas[~(zerado | baixo | alto)].copy()
    vendas["Valor_Venda"] = vendas["Valor_Venda"].round(2)

    # Liga cada venda aos cadastros pela chave normalizada.
    vendas["chave_regional"] = criar_chave(vendas["Região"])
    vendas["chave_canal"] = criar_chave(vendas["Canal"])
    vendas["chave_produto"] = criar_chave(vendas["Produto"])

    regional_aux = regional.assign(chave_regional=criar_chave(regional["nome"]))
    canal_aux = canal.assign(chave_canal=criar_chave(canal["nome"]))
    produto_aux = produto.assign(chave_produto=criar_chave(produto["nome"]))

    vendas = vendas.merge(
        regional_aux[["chave_regional", "regional_sk"]], on="chave_regional", how="left"
    )
    vendas = vendas.merge(
        canal_aux[["chave_canal", "canal_sk", "comissao_pct"]], on="chave_canal", how="left"
    )
    vendas = vendas.merge(
        produto_aux[["chave_produto", "produto_sk", "produto_id"]], on="chave_produto", how="left"
    )

    sem_cadastro = vendas[["regional_sk", "canal_sk", "produto_sk"]].isna().any(axis=1)
    rejeitados.append(
        rejeitar(
            vendas.loc[sem_cadastro, ["linha_planilha", "Data", "Região", "Canal", "Produto", "Valor_Venda"]],
            "planilha", "Sem correspondência no cadastro",
        )
    )
    vendas = vendas[~sem_cadastro].copy()

    # Cada venda usa o preço e o custo do seu próprio ano.
    vendas["ano"] = vendas["Data"].dt.year
    vendas = vendas.merge(precos, on=["produto_id", "ano"], how="left")

    vendas["tempo_id"] = vendas["Data"].dt.year * 100 + vendas["Data"].dt.month
    vendas["valor_venda"] = vendas["Valor_Venda"]
    vendas["quantidade_estimada"] = vendas["valor_venda"] / vendas["preco_venda"]
    vendas["custo_estimado"] = vendas["quantidade_estimada"] * vendas["custo_unitario"]
    vendas["comissao"] = vendas["valor_venda"] * vendas["comissao_pct"] / 100
    vendas["margem_estimada"] = (
        vendas["valor_venda"] - vendas["custo_estimado"] - vendas["comissao"]
    )

    colunas_valor = ["quantidade_estimada", "custo_estimado", "comissao", "margem_estimada"]
    vendas[colunas_valor] = vendas[colunas_valor].round(2)
    vendas = vendas.sort_values("linha_planilha")
    vendas["venda_sk"] = range(1, len(vendas) + 1)

    fato = vendas[["venda_sk", "tempo_id", "produto_sk", "canal_sk", "regional_sk",
                   "linha_planilha", "valor_venda", *colunas_valor]]
    return fato, pd.concat(rejeitados, ignore_index=True)

def tratar_metas(brutos, regional):
    metas = brutos["metas_mensais"].sort_values("meta_id").copy()

    sem_valor = metas["valor_meta"].isna()
    sem_regional = ~metas["regional_id"].isin(regional["regional_id"])

    # Meta repetida para a mesma regional e mês: vale a mais recente.
    validas = metas[~(sem_valor | sem_regional)]
    substituida = validas.duplicated(subset=["regional_id", "competencia"], keep="last")

    rejeitados = pd.concat([
        rejeitar(metas[sem_valor], "metas_mensais", "Meta sem valor"),
        rejeitar(metas[sem_regional], "metas_mensais", "Regional inexistente"),
        rejeitar(validas[substituida], "metas_mensais", "Substituída por meta mais recente"),
    ], ignore_index=True)

    metas = validas[~substituida].copy()
    competencia = pd.to_datetime(metas["competencia"], format="%m/%Y")
    metas["tempo_id"] = competencia.dt.year * 100 + competencia.dt.month
    metas = metas.merge(regional[["regional_id", "regional_sk"]], on="regional_id")
    return metas[["tempo_id", "regional_sk", "valor_meta"]], rejeitados

# ---------------------------------------------------------------------
# 3. CARGA: grava no DW usando as tabelas criadas pelo 02_dw_estrela.sql
# ---------------------------------------------------------------------
def carregar(tabelas):
    conexao = sqlite3.connect(CAMINHO_DW)
    conexao.execute("PRAGMA foreign_keys = ON")

    # Apaga primeiro quem depende das dimensões (as tabelas fato).
    for tabela in reversed(list(tabelas)):
        conexao.execute(f"DELETE FROM {tabela}")
    conexao.commit()

    # if_exists="append" mantém o CREATE TABLE do arquivo SQL.
    # "replace" recriaria a tabela e perderia chaves, NOT NULL e CHECK.
    for tabela, df in tabelas.items():
        df.to_sql(tabela, conexao, if_exists="append", index=False)
        print(f"  {tabela:<22} {len(df):>4} linhas")

    conexao.close()

# ---------------------------------------------------------------------
# 4. VALIDAÇÃO: confere se nenhuma linha se perdeu
# ---------------------------------------------------------------------
def validar(brutos):
    conexao = sqlite3.connect(CAMINHO_DW)

    consulta = """
        SELECT
            (SELECT COUNT(*) FROM fato_vendas) AS vendas,
            (SELECT COUNT(*) FROM fato_metas) AS metas,
            (SELECT COUNT(*) FROM auditoria_rejeitados
              WHERE fonte = 'planilha') AS vendas_rejeitadas,
            (SELECT COUNT(*) FROM auditoria_rejeitados
              WHERE fonte = 'metas_mensais') AS metas_rejeitadas
    """
    total = pd.read_sql_query(consulta, conexao).iloc[0]

    # Toda linha lida precisa estar em um fato ou na auditoria.
    if total["vendas"] + total["vendas_rejeitadas"] != len(brutos["vendas"]):
        raise ValueError("Linhas da planilha não conferem com o DW.")
    if total["metas"] + total["metas_rejeitadas"] != len(brutos["metas_mensais"]):
        raise ValueError("Linhas de metas não conferem com o DW.")
    print("  Contagem conferida: toda linha lida está em um fato ou na auditoria.")

    print("\nRejeitados por motivo:")
    print(pd.read_sql_query("""
        SELECT fonte, motivo, COUNT(*) AS linhas
        FROM auditoria_rejeitados
        GROUP BY fonte, motivo
        ORDER BY fonte, linhas DESC
    """, conexao).to_string(index=False))

    print("\nResultado por ano:")
    print(pd.read_sql_query("""
        SELECT t.ano,
               ROUND(SUM(f.valor_venda), 2) AS faturamento,
               ROUND(SUM(f.margem_estimada), 2) AS margem_estimada
        FROM fato_vendas AS f
        JOIN dim_tempo AS t ON t.tempo_id = f.tempo_id
        GROUP BY t.ano
        ORDER BY t.ano
    """, conexao).to_string(index=False))

    print("\nMeta x realizado em 2025 (faturamento das 3 cidades com meta):")
    print(pd.read_sql_query("""
        WITH realizado AS (
            SELECT tempo_id, regional_sk, SUM(valor_venda) AS valor
            FROM fato_vendas
            GROUP BY tempo_id, regional_sk
        )
        SELECT r.nome AS regional,
               ROUND(SUM(m.valor_meta), 2) AS meta,
               ROUND(SUM(COALESCE(v.valor, 0)), 2) AS realizado,
               ROUND(100.0 * SUM(COALESCE(v.valor, 0)) / SUM(m.valor_meta), 1) AS atingimento_pct
        FROM fato_metas AS m
        JOIN dim_regional AS r ON r.regional_sk = m.regional_sk
        JOIN dim_tempo AS t ON t.tempo_id = m.tempo_id
        LEFT JOIN realizado AS v
               ON v.tempo_id = m.tempo_id AND v.regional_sk = m.regional_sk
        WHERE t.ano = 2025
        GROUP BY r.nome
        ORDER BY r.nome
    """, conexao).to_string(index=False))

    conexao.close()

# ---------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------
def main():
    print("1. Extraindo as fontes...")
    brutos = extrair()

    print("\n2. Tratando os dados...")
    regional = tratar_regional(brutos)
    canal = tratar_canal(brutos)
    produto = tratar_produto(brutos)
    precos = tratar_precos(brutos)
    tempo = tratar_tempo(brutos["vendas"])
    fato_vendas, vendas_rejeitadas = tratar_vendas(brutos, regional, canal, produto, precos)
    fato_metas, metas_rejeitadas = tratar_metas(brutos, regional)

    print("\n3. Carregando o Data Warehouse...")
    # A ordem importa: dimensões primeiro, porque os fatos apontam para elas.
    carregar({
        "dim_tempo": tempo,
        "dim_produto": produto[["produto_sk", "codigo", "nome", "categoria", "unidade_venda",
                                "fornecedor", "fornecedor_uf", "ativo"]],
        "dim_canal": canal[["canal_sk", "nome", "descricao", "comissao_pct"]],
        "dim_regional": regional[["regional_sk", "nome", "tipo", "uf", "macrorregiao",
                                  "gerente", "data_inicio_operacao"]],
        "fato_vendas": fato_vendas,
        "fato_metas": fato_metas,
        "auditoria_rejeitados": pd.concat([vendas_rejeitadas, metas_rejeitadas], ignore_index=True),
    })

    print("\n4. Validando a carga...")
    validar(brutos)
    print("\nPipeline concluído.")

if __name__ == "__main__":
    main()
