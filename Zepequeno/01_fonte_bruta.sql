-- =====================================================================
-- Zé Pequeno - FONTE DE DADOS BRUTA (simula o sistema operacional da empresa)
-- Complementa a planilha tabela_vendas_ZePequeno_corrigido.xlsx
--
-- Dados FICTÍCIOS, criados para a aula.
-- De propósito este banco NÃO tem chaves estrangeiras nem CHECKs, e guarda
-- valores como texto: assim os problemas abaixo conseguem entrar nele,
-- como acontece em sistemas reais.
--
-- Problemas plantados para os alunos encontrarem:
--   regionais      -> espaços nos nomes, UF minúscula, datas em 2 formatos,
--                     gerente sem nome
--   produtos       -> produto PCA-01 cadastrado duas vezes
--   precos_produto -> números como texto ('R$ 92,50', '85,00'), custo nulo
--   canais         -> comissão como texto ('3,5%')
--   metas_mensais  -> meta nula, meta revisada (registro repetido) e
--                     regional_id 99, que não existe
--
-- Como criar:  sqlite3 zepequeno_bruto.sqlite < 01_fonte_bruta.sql
-- =====================================================================

DROP TABLE IF EXISTS metas_mensais;
DROP TABLE IF EXISTS precos_produto;
DROP TABLE IF EXISTS produtos;
DROP TABLE IF EXISTS fornecedores;
DROP TABLE IF EXISTS canais;
DROP TABLE IF EXISTS regionais;

-- Onde a empresa atua. O "nome" é o texto da coluna Região da planilha,
-- que mistura cidades e macrorregiões.
CREATE TABLE regionais (
    regional_id          INTEGER PRIMARY KEY,
    nome                 TEXT,
    tipo                 TEXT,
    uf                   TEXT,
    macrorregiao         TEXT,
    gerente              TEXT,
    data_inicio_operacao TEXT
);

INSERT INTO regionais VALUES
(1,  'Joinville',       'Cidade',       'SC', 'Sul',          'Marina Souza',    '15/03/2018'),
(2,  'Blumenau ',       'Cidade',       'sc', 'Sul',          'Carlos Winter',   '2019-06-01'),
(3,  ' Florianópolis',  'Cidade',       'SC', 'Sul',          'Paula Ramos',     '01/02/2020'),
(4,  'Curitiba',        'Cidade',       'pr', 'Sul',          NULL,              '2023-11-10'),
(5,  'São Paulo',       'Cidade',       'SP', 'Sudeste',      'Rafael Nunes',    '09/01/2023'),
(6,  'Rio de Janeiro ', 'Cidade',       'rj', 'Sudeste',      'Bruna Teixeira',  '2023-05-02'),
(7,  'Sul',             'Macrorregião', NULL, 'Sul',          NULL,              NULL),
(8,  'Sudeste',         'Macrorregião', NULL, 'Sudeste',      NULL,              NULL),
(9,  'Nordeste',        'Macrorregião', NULL, 'Nordeste',     NULL,              NULL),
(10, 'Norte',           'Macrorregião', NULL, 'Norte',        NULL,              NULL),
(11, 'Centro-Oeste',    'Macrorregião', NULL, 'Centro-Oeste', NULL,              NULL);

CREATE TABLE canais (
    canal_id  INTEGER PRIMARY KEY,
    nome      TEXT,
    descricao TEXT,
    comissao  TEXT   -- percentual pago sobre a venda, guardado como texto
);

INSERT INTO canais VALUES
(1, 'Loja Física', 'Venda no balcão das lojas próprias', '3,5%'),
(2, 'E-commerce',  'Site próprio e marketplaces',        '12%');

CREATE TABLE fornecedores (
    fornecedor_id INTEGER PRIMARY KEY,
    razao_social  TEXT,
    cidade        TEXT,
    uf            TEXT
);

INSERT INTO fornecedores VALUES
(1, 'Doces Serra Azul Ltda',     'Gaspar',  'SC'),
(2, 'Amendoim Campo Verde Ltda', 'Marília', 'SP'),
(3, 'Embalagens Litoral Ltda',   'Itajaí',  'SC');

CREATE TABLE produtos (
    produto_id    INTEGER PRIMARY KEY,
    codigo        TEXT,
    nome          TEXT,
    categoria     TEXT,
    unidade_venda TEXT,
    fornecedor_id INTEGER,
    ativo         INTEGER   -- 1 = ativo, 0 = inativo
);

INSERT INTO produtos VALUES
(1, 'PCA-01', 'Paçoca',        'Doces de amendoim', 'Caixa', 1, 1),
(2, 'ROL-01', 'Rolhas',        'Vinhos', 'Caixa', 2, 1),
(3, 'PDM-01', 'Pé de Moleque', 'Doces de amendoim', 'Caixa', 1, 1),  -- ainda sem vendas
(4, 'PCA-01', 'PAÇOCA ',       'Doces de amendoim', 'Caixa', 1, 1);  -- duplicado

-- Preço e custo de UMA CAIXA em cada ano. A planilha só traz o valor vendido,
-- então é esta tabela que permite estimar quantidade, custo e margem.
CREATE TABLE precos_produto (
    produto_id     INTEGER,
    ano            INTEGER,
    preco_venda    TEXT,
    custo_unitario TEXT,
    PRIMARY KEY (produto_id, ano)
);

INSERT INTO precos_produto VALUES
(1, 2022, '78,00',    '41,00'),
(1, 2023, '82,90',    '43,50'),
(1, 2024, 'R$ 88,00', 'R$ 47,00'),
(1, 2025, 'R$ 92,50', 'R$ 50,00'),
(1, 2026, '96.00',    '52.00'),
(2, 2022, '64,00',    '36,00'),
(2, 2023, '67,50',    '38,00'),
(2, 2024, 'R$ 71,00', NULL),
(2, 2025, 'R$ 75,00', 'R$ 43,00'),
(2, 2026, '79.00',    '45.00');

-- Meta mensal de faturamento das 3 principais cidades.
-- Os registros finais (meta_id 181 em diante) são revisões e erros de digitação.
CREATE TABLE metas_mensais (
    meta_id     INTEGER PRIMARY KEY,
    regional_id INTEGER,
    competencia TEXT,   -- formato MM/AAAA
    valor_meta  REAL
);

INSERT INTO metas_mensais VALUES
(1, 1, '01/2022', 9600.00),
(2, 2, '01/2022', 4300.00),
(3, 3, '01/2022', 4000.00),
(4, 1, '02/2022', 8900.00),
(5, 2, '02/2022', 4900.00),
(6, 3, '02/2022', 4300.00),
(7, 1, '03/2022', 10000.00),
(8, 2, '03/2022', 4400.00),
(9, 3, '03/2022', 4100.00),
(10, 1, '04/2022', 8600.00),
(11, 2, '04/2022', 4500.00),
(12, 3, '04/2022', 4100.00),
(13, 1, '05/2022', 8600.00),
(14, 2, '05/2022', 4500.00),
(15, 3, '05/2022', 4300.00),
(16, 1, '06/2022', 9500.00),
(17, 2, '06/2022', 4500.00),
(18, 3, '06/2022', 4200.00),
(19, 1, '07/2022', 9900.00),
(20, 2, '07/2022', 4300.00),
(21, 3, '07/2022', 4400.00),
(22, 1, '08/2022', 9700.00),
(23, 2, '08/2022', 4600.00),
(24, 3, '08/2022', 3900.00),
(25, 1, '09/2022', 10200.00),
(26, 2, '09/2022', 4600.00),
(27, 3, '09/2022', 3800.00),
(28, 1, '10/2022', 8700.00),
(29, 2, '10/2022', 5000.00),
(30, 3, '10/2022', 4200.00),
(31, 1, '11/2022', 9900.00),
(32, 2, '11/2022', 4900.00),
(33, 3, '11/2022', 4200.00),
(34, 1, '12/2022', 10200.00),
(35, 2, '12/2022', 4600.00),
(36, 3, '12/2022', 4200.00),
(37, 1, '01/2023', 19100.00),
(38, 2, '01/2023', 16300.00),
(39, 3, '01/2023', 17500.00),
(40, 1, '02/2023', 18300.00),
(41, 2, '02/2023', 16500.00),
(42, 3, '02/2023', 15100.00),
(43, 1, '03/2023', 17200.00),
(44, 2, '03/2023', 15400.00),
(45, 3, '03/2023', 15200.00),
(46, 1, '04/2023', 17200.00),
(47, 2, '04/2023', 14800.00),
(48, 3, '04/2023', 15800.00),
(49, 1, '05/2023', 18500.00),
(50, 2, '05/2023', 15600.00),
(51, 3, '05/2023', 16100.00),
(52, 1, '06/2023', 17100.00),
(53, 2, '06/2023', 15300.00),
(54, 3, '06/2023', 17700.00),
(55, 1, '07/2023', 18600.00),
(56, 2, '07/2023', 16300.00),
(57, 3, '07/2023', 15500.00),
(58, 1, '08/2023', 18800.00),
(59, 2, '08/2023', 15000.00),
(60, 3, '08/2023', 16100.00),
(61, 1, '09/2023', 19700.00),
(62, 2, '09/2023', 16400.00),
(63, 3, '09/2023', 16600.00),
(64, 1, '10/2023', 18700.00),
(65, 2, '10/2023', 16900.00),
(66, 3, '10/2023', 17300.00),
(67, 1, '11/2023', 17200.00),
(68, 2, '11/2023', 14600.00),
(69, 3, '11/2023', 15900.00),
(70, 1, '12/2023', 17300.00),
(71, 2, '12/2023', 15100.00),
(72, 3, '12/2023', 17800.00),
(73, 1, '01/2024', 11400.00),
(74, 2, '01/2024', 9600.00),
(75, 3, '01/2024', 9900.00),
(76, 1, '02/2024', 10500.00),
(77, 2, '02/2024', 10600.00),
(78, 3, '02/2024', 9500.00),
(79, 1, '03/2024', 10300.00),
(80, 2, '03/2024', NULL),
(81, 3, '03/2024', 9200.00),
(82, 1, '04/2024', 10800.00),
(83, 2, '04/2024', 9500.00),
(84, 3, '04/2024', 9700.00),
(85, 1, '05/2024', 11500.00),
(86, 2, '05/2024', 9700.00),
(87, 3, '05/2024', 9100.00),
(88, 1, '06/2024', 11700.00),
(89, 2, '06/2024', 9900.00),
(90, 3, '06/2024', 8900.00),
(91, 1, '07/2024', 9800.00),
(92, 2, '07/2024', 9200.00),
(93, 3, '07/2024', 9800.00),
(94, 1, '08/2024', 11300.00),
(95, 2, '08/2024', 9800.00),
(96, 3, '08/2024', 8800.00),
(97, 1, '09/2024', 10500.00),
(98, 2, '09/2024', 10800.00),
(99, 3, '09/2024', 9600.00),
(100, 1, '10/2024', 11600.00),
(101, 2, '10/2024', 10500.00),
(102, 3, '10/2024', 8800.00),
(103, 1, '11/2024', 11100.00),
(104, 2, '11/2024', 10200.00),
(105, 3, '11/2024', 9700.00),
(106, 1, '12/2024', 10300.00),
(107, 2, '12/2024', 10100.00),
(108, 3, '12/2024', 8900.00),
(109, 1, '01/2025', 8200.00),
(110, 2, '01/2025', 6800.00),
(111, 3, '01/2025', 8300.00),
(112, 1, '02/2025', 8800.00),
(113, 2, '02/2025', 6600.00),
(114, 3, '02/2025', 7700.00),
(115, 1, '03/2025', 7800.00),
(116, 2, '03/2025', 7400.00),
(117, 3, '03/2025', 8200.00),
(118, 1, '04/2025', 8000.00),
(119, 2, '04/2025', 7000.00),
(120, 3, '04/2025', 7800.00),
(121, 1, '05/2025', 7800.00),
(122, 2, '05/2025', 7200.00),
(123, 3, '05/2025', 7700.00),
(124, 1, '06/2025', 8700.00),
(125, 2, '06/2025', 6900.00),
(126, 3, '06/2025', 7000.00),
(127, 1, '07/2025', 8000.00),
(128, 2, '07/2025', 6300.00),
(129, 3, '07/2025', 8300.00),
(130, 1, '08/2025', 8800.00),
(131, 2, '08/2025', 7300.00),
(132, 3, '08/2025', NULL),
(133, 1, '09/2025', 8000.00),
(134, 2, '09/2025', 6300.00),
(135, 3, '09/2025', 8200.00),
(136, 1, '10/2025', 8900.00),
(137, 2, '10/2025', 6400.00),
(138, 3, '10/2025', 7700.00),
(139, 1, '11/2025', 7600.00),
(140, 2, '11/2025', 7200.00),
(141, 3, '11/2025', 8000.00),
(142, 1, '12/2025', 7700.00),
(143, 2, '12/2025', 6800.00),
(144, 3, '12/2025', 7700.00),
(145, 1, '01/2026', 16200.00),
(146, 2, '01/2026', 16700.00),
(147, 3, '01/2026', 16000.00),
(148, 1, '02/2026', 16000.00),
(149, 2, '02/2026', 15800.00),
(150, 3, '02/2026', 16900.00),
(151, 1, '03/2026', 16000.00),
(152, 2, '03/2026', 15100.00),
(153, 3, '03/2026', 17700.00),
(154, 1, '04/2026', 17300.00),
(155, 2, '04/2026', 15500.00),
(156, 3, '04/2026', 16300.00),
(157, 1, '05/2026', 15700.00),
(158, 2, '05/2026', 14900.00),
(159, 3, '05/2026', 15800.00),
(160, 1, '06/2026', 17100.00),
(161, 2, '06/2026', 14900.00),
(162, 3, '06/2026', 15500.00),
(163, 1, '07/2026', 15600.00),
(164, 2, '07/2026', 16000.00),
(165, 3, '07/2026', 15500.00),
(166, 1, '08/2026', 18100.00),
(167, 2, '08/2026', 16700.00),
(168, 3, '08/2026', 15000.00),
(169, 1, '09/2026', 16100.00),
(170, 2, '09/2026', 16100.00),
(171, 3, '09/2026', 15400.00),
(172, 1, '10/2026', 15800.00),
(173, 2, '10/2026', 16900.00),
(174, 3, '10/2026', 16500.00),
(175, 1, '11/2026', NULL),
(176, 2, '11/2026', 15600.00),
(177, 3, '11/2026', 17100.00),
(178, 1, '12/2026', 17800.00),
(179, 2, '12/2026', 14800.00),
(180, 3, '12/2026', 15100.00),
(181, 1, '05/2024', 11800.00),
(182, 3, '10/2025', 8300.00),
(183, 99, '01/2025', 9000.00),
(184, 99, '02/2025', 9200.00);
