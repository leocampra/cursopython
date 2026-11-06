-- =====================================================================
-- Zé Pequeno - DATA WAREHOUSE (modelo estrela)
-- Destino dos dados já tratados pelo 03_pipeline.py
--
--   Dimensões: dim_tempo, dim_produto, dim_canal, dim_regional
--   Fatos:     fato_vendas (1 linha = 1 lançamento da planilha)
--              fato_metas  (1 linha = meta de 1 regional em 1 mês)
--   Auditoria: registros recusados pelo tratamento, com o motivo
--
-- Ao contrário do banco bruto, aqui as regras ficam no próprio banco:
-- tipos corretos, NOT NULL, CHECK e chaves estrangeiras.
--
-- Como criar:  sqlite3 zepequeno_dw.sqlite < 02_dw_estrela.sql
-- =====================================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS fato_vendas;
DROP TABLE IF EXISTS fato_metas;
DROP TABLE IF EXISTS auditoria_rejeitados;
DROP TABLE IF EXISTS dim_tempo;
DROP TABLE IF EXISTS dim_produto;
DROP TABLE IF EXISTS dim_canal;
DROP TABLE IF EXISTS dim_regional;

-- Um registro por mês, inclusive meses sem venda: a planilha só tem
-- lançamentos mensais (sempre no dia 1º).
CREATE TABLE dim_tempo (
    tempo_id    INTEGER PRIMARY KEY,   -- AAAAMM, ex.: 202503
    data_inicio TEXT    NOT NULL UNIQUE,
    ano         INTEGER NOT NULL,
    semestre    INTEGER NOT NULL CHECK (semestre BETWEEN 1 AND 2),
    trimestre   INTEGER NOT NULL CHECK (trimestre BETWEEN 1 AND 4),
    mes         INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    nome_mes    TEXT    NOT NULL
);

CREATE TABLE dim_produto (
    produto_sk    INTEGER PRIMARY KEY,   -- chave substituta (surrogate key)
    codigo        TEXT    NOT NULL UNIQUE,
    nome          TEXT    NOT NULL,
    categoria     TEXT    NOT NULL,
    unidade_venda TEXT    NOT NULL,
    fornecedor    TEXT    NOT NULL,
    fornecedor_uf TEXT    NOT NULL,
    ativo         INTEGER NOT NULL CHECK (ativo IN (0, 1))
);

CREATE TABLE dim_canal (
    canal_sk     INTEGER PRIMARY KEY,
    nome         TEXT NOT NULL UNIQUE,
    descricao    TEXT NOT NULL,
    comissao_pct REAL NOT NULL CHECK (comissao_pct >= 0)
);

CREATE TABLE dim_regional (
    regional_sk          INTEGER PRIMARY KEY,
    nome                 TEXT NOT NULL UNIQUE,
    tipo                 TEXT NOT NULL CHECK (tipo IN ('Cidade', 'Macrorregião')),
    uf                   TEXT NOT NULL,   -- 'N/A' para macrorregiões
    macrorregiao         TEXT NOT NULL,
    gerente              TEXT NOT NULL,   -- 'Não informado' quando vazio
    data_inicio_operacao TEXT             -- AAAA-MM-DD; vazia nas macrorregiões
);

CREATE TABLE fato_vendas (
    venda_sk            INTEGER PRIMARY KEY,
    tempo_id            INTEGER NOT NULL REFERENCES dim_tempo (tempo_id),
    produto_sk          INTEGER NOT NULL REFERENCES dim_produto (produto_sk),
    canal_sk            INTEGER NOT NULL REFERENCES dim_canal (canal_sk),
    regional_sk         INTEGER NOT NULL REFERENCES dim_regional (regional_sk),
    linha_planilha      INTEGER NOT NULL UNIQUE,   -- rastreabilidade até o Excel
    valor_venda         REAL    NOT NULL CHECK (valor_venda > 0),
    -- Estimativas: a planilha não informa quantidade nem custo.
    quantidade_estimada REAL    NOT NULL,   -- valor_venda / preço da caixa no ano
    custo_estimado      REAL    NOT NULL,   -- quantidade x custo da caixa no ano
    comissao            REAL    NOT NULL,   -- valor_venda x comissão do canal
    margem_estimada     REAL    NOT NULL    -- valor - custo - comissão
);

CREATE TABLE fato_metas (
    tempo_id    INTEGER NOT NULL REFERENCES dim_tempo (tempo_id),
    regional_sk INTEGER NOT NULL REFERENCES dim_regional (regional_sk),
    valor_meta  REAL    NOT NULL CHECK (valor_meta > 0),
    PRIMARY KEY (tempo_id, regional_sk)
);

-- Nada some em silêncio: o que não entra nos fatos fica aqui.
CREATE TABLE auditoria_rejeitados (
    rejeitado_id INTEGER PRIMARY KEY,
    fonte        TEXT NOT NULL,   -- de onde veio o registro
    motivo       TEXT NOT NULL,
    registro     TEXT NOT NULL    -- conteúdo original da linha
);

CREATE INDEX idx_vendas_tempo    ON fato_vendas (tempo_id);
CREATE INDEX idx_vendas_produto  ON fato_vendas (produto_sk);
CREATE INDEX idx_vendas_canal    ON fato_vendas (canal_sk);
CREATE INDEX idx_vendas_regional ON fato_vendas (regional_sk);
