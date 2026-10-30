-- TABELA: clientes
CREATE TABLE clientes (
    cliente_id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cidade TEXT NOT NULL,
    data_cadastro TEXT NOT NULL
);

-- TABELA: itens
CREATE TABLE itens (
    item_id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('produto', 'servico')),
    categoria TEXT NOT NULL,
    preco_atual REAL NOT NULL CHECK (preco_atual >= 0)
);

-- TABELA: unidades
CREATE TABLE unidades (
    unidade_id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    cidade TEXT NOT NULL,
    estado TEXT NOT NULL
);

-- TABELA: vendas
CREATE TABLE vendas (
    venda_id INTEGER PRIMARY KEY,
    unidade_id INTEGER NOT NULL,
    cliente_id INTEGER NOT NULL,
    data_venda TEXT NOT NULL,
    forma_pagamento TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('concluida', 'cancelada')),
    FOREIGN KEY (unidade_id) REFERENCES unidades(unidade_id),
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
);

-- TABELA: itens_venda
CREATE TABLE itens_venda (
    item_venda_id INTEGER PRIMARY KEY,
    venda_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario REAL NOT NULL CHECK (preco_unitario >= 0),
    desconto REAL NOT NULL DEFAULT 0 CHECK (desconto >= 0),
    FOREIGN KEY (venda_id) REFERENCES vendas(venda_id),
    FOREIGN KEY (item_id) REFERENCES itens(item_id)
);

-- COLUNAS: cliente_id, nome, cidade, data_cadastro
INSERT INTO clientes (cliente_id, nome, cidade, data_cadastro) VALUES (1, 'Ana Souza', 'Guanhães', '2025-01-12');
INSERT INTO clientes (cliente_id, nome, cidade, data_cadastro) VALUES (2, 'Bruno Lima', 'Guanhães', '2025-02-03');
INSERT INTO clientes (cliente_id, nome, cidade, data_cadastro) VALUES (3, 'Carla Mendes', 'Ipatinga', '2025-02-19');
INSERT INTO clientes (cliente_id, nome, cidade, data_cadastro) VALUES (4, 'Diego Alves', 'Guanhães', '2025-03-05');
INSERT INTO clientes (cliente_id, nome, cidade, data_cadastro) VALUES (5, 'Elisa Rocha', 'Ipatinga', '2025-04-22');
INSERT INTO clientes (cliente_id, nome, cidade, data_cadastro) VALUES (6, 'Felipe Costa', 'Guanhães', '2025-05-16');
INSERT INTO clientes (cliente_id, nome, cidade, data_cadastro) VALUES (7, 'Gabi Nunes', 'Ipatinga', '2025-06-01');
INSERT INTO clientes (cliente_id, nome, cidade, data_cadastro) VALUES (8, 'Heitor Reis', 'Guanhães', '2025-06-20');

-- COLUNAS: item_id, nome, tipo, categoria, preco_atual
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (1, 'Ração Premium 10kg', 'produto', 'Alimentação', 189.9);
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (2, 'Ração Filhote 3kg', 'produto', 'Alimentação', 79.9);
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (3, 'Brinquedo Mordedor', 'produto', 'Brinquedos', 24.9);
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (4, 'Coleira Ajustável', 'produto', 'Acessórios', 39.9);
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (5, 'Areia Higiênica', 'produto', 'Higiene', 32.5);
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (6, 'Banho', 'servico', 'Estética', 55.0);
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (7, 'Tosa', 'servico', 'Estética', 45.0);
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (8, 'Banho e Tosa', 'servico', 'Estética', 89.9);
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (9, 'Consulta Veterinária', 'servico', 'Veterinário', 120.0);
INSERT INTO itens (item_id, nome, tipo, categoria, preco_atual) VALUES (10, 'Antipulgas', 'produto', 'Saúde', 68.0);

-- COLUNAS: unidade_id, nome, cidade, estado
INSERT INTO unidades (unidade_id, nome, cidade, estado) VALUES (1, 'Pet Shop Centro', 'Guanhães', 'MG');
INSERT INTO unidades (unidade_id, nome, cidade, estado) VALUES (2, 'Pet Shop Jardim', 'Guanhães', 'MG');
INSERT INTO unidades (unidade_id, nome, cidade, estado) VALUES (3, 'Pet Shop Serra', 'Ipatinga', 'MG');

-- COLUNAS: venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1001, 1, 1, '2025-01-05', 'Pix', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1002, 1, 2, '2025-01-08', 'Cartão', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1003, 2, 3, '2025-01-15', 'Dinheiro', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1004, 1, 4, '2025-02-02', 'Pix', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1005, 3, 5, '2025-02-10', 'Cartão', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1006, 2, 1, '2025-02-17', 'Pix', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1007, 1, 6, '2025-03-03', 'Cartão', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1008, 3, 7, '2025-03-11', 'Pix', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1009, 2, 8, '2025-03-22', 'Dinheiro', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1010, 1, 3, '2025-04-04', 'Pix', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1011, 3, 5, '2025-04-12', 'Cartão', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1012, 2, 4, '2025-04-19', 'Pix', 'cancelada');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1013, 1, 2, '2025-05-06', 'Cartão', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1014, 2, 6, '2025-05-14', 'Pix', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1015, 3, 7, '2025-05-28', 'Cartão', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1016, 1, 8, '2025-06-02', 'Pix', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1017, 2, 1, '2025-06-09', 'Dinheiro', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1018, 3, 3, '2025-06-21', 'Cartão', 'concluida');
INSERT INTO vendas (venda_id, unidade_id, cliente_id, data_venda, forma_pagamento, status) VALUES (1019, 1, 5, '2025-07-07', 'Pix', 'concluida');

-- COLUNAS: item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (1, 1001, 1, 1, 189.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (2, 1001, 6, 1, 55.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (3, 1002, 3, 2, 24.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (4, 1002, 4, 1, 39.9, 5.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (5, 1003, 8, 1, 89.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (6, 1003, 10, 1, 68.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (7, 1004, 2, 1, 79.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (8, 1004, 7, 1, 45.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (9, 1005, 9, 1, 120.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (10, 1005, 10, 1, 68.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (11, 1006, 6, 1, 55.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (12, 1006, 5, 2, 32.5, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (13, 1007, 1, 1, 189.9, 10.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (14, 1007, 3, 1, 24.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (15, 1008, 8, 1, 89.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (16, 1008, 4, 2, 39.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (17, 1009, 2, 2, 79.9, 5.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (18, 1009, 6, 1, 55.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (19, 1010, 10, 1, 68.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (20, 1010, 7, 1, 45.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (21, 1011, 9, 1, 120.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (22, 1011, 6, 1, 55.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (23, 1012, 8, 1, 89.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (24, 1013, 1, 1, 189.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (25, 1013, 5, 1, 32.5, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (26, 1014, 6, 1, 55.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (27, 1014, 7, 1, 45.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (28, 1015, 10, 2, 68.0, 8.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (29, 1015, 3, 1, 24.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (30, 1016, 2, 1, 79.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (31, 1016, 8, 1, 89.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (32, 1017, 4, 1, 39.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (33, 1017, 5, 1, 32.5, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (34, 1018, 9, 1, 120.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (35, 1018, 6, 1, 55.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (36, 1019, 1, 1, 189.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (37, 1019, 10, 1, 68.0, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (38, 1020, 8, 1, 89.9, 0.0);
INSERT INTO itens_venda (item_venda_id, venda_id, item_id, quantidade, preco_unitario, desconto) VALUES (39, 1020, 3, 3, 24.9, 4.9);