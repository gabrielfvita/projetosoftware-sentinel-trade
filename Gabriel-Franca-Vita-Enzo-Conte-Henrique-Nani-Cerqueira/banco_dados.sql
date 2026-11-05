CREATE TABLE IF NOT EXISTS 'investidores'(
    id_investidor INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    status ENUM('ativo', 'inativo') NOT NULL DEFAULT 'ativo'
);

CREATE TABLE IF NOT EXISTS 'conta'(
    id_conta INT PRIMARY KEY AUTO_INCREMENT,
    id_investidor INT NOT NULL REFERENCES 'investidores'(id_investidor) ON DELETE CASCADE,
    saldo_disponivel DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    limite_financeiro DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    situacao_conta ENUM('ativa', 'suspensa', 'encerrada') NOT NULL DEFAULT 'ativa'
);

CREATE TABLE IF NOT EXISTS 'ativos'(
    codigo_ativo VARCHAR(10) PRIMARY KEY,
    nome_ativo VARCHAR(100) NOT NULL,
    tipo_ativo ENUM('ação', 'fundo', 'título') NOT NULL
);

CREATE TABLE IF NOT EXISTS 'posicao'(
    id_posicao INT PRIMARY KEY AUTO_INCREMENT,
    id_conta INT NOT NULL REFERENCES 'conta'(id_conta) ON DELETE CASCADE,
    codigo_ativo VARCHAR(10) NOT NULL REFERENCES 'ativos'(codigo_ativo) ON DELETE CASCADE,
    quantidade INT NOT NULL DEFAULT 0,
    valor_medio DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS 'ordem'(
    id_ordem INT PRIMARY KEY AUTO_INCREMENT,
    id_conta INT NOT NULL REFERENCES 'conta'(id_conta) ON DELETE CASCADE,
    codigo_ativo VARCHAR(10) NOT NULL REFERENCES 'ativos'(codigo_ativo) ON DELETE CASCADE,
    tipo_ordem ENUM('compra', 'venda') NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10, 2) NOT NULL,
    status_ordem ENUM('pendente', 'executada', 'cancelada') NOT NULL DEFAULT 'pendente',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_execucao TIMESTAMP NULL DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS 'auditoria'(
    id_auditoria INT PRIMARY KEY AUTO_INCREMENT,
    id_conta INT NOT NULL REFERENCES 'conta'(id_conta) ON DELETE CASCADE,
    tipo_operacao VARCHAR(50) NOT NULL,
    descricao TEXT,
    data_operacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);