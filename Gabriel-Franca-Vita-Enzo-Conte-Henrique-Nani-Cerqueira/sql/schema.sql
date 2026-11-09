CREATE TABLE investidores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    senha_hash VARCHAR(255) NOT NULL,
    mfa_habilitado BOOLEAN NOT NULL DEFAULT 1,
    status VARCHAR(20) NOT NULL DEFAULT 'ativo'
);

CREATE TABLE contas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    investidor_id INTEGER NOT NULL,
    saldo_disponivel REAL NOT NULL DEFAULT 0,
    limite_risco REAL NOT NULL,
    situacao VARCHAR(20) NOT NULL DEFAULT 'ativa',

    FOREIGN KEY (investidor_id)
        REFERENCES investidores(id)
);

CREATE TABLE ativos (
    codigo VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    cotacao REAL NOT NULL
);

CREATE TABLE posicoes_carteira (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conta_id INTEGER NOT NULL,
    codigo_ativo VARCHAR(10) NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    quantidade_disponivel INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (conta_id)
        REFERENCES contas(id),

    FOREIGN KEY (codigo_ativo)
        REFERENCES ativos(codigo),

    UNIQUE (conta_id, codigo_ativo)
);

CREATE TABLE ordens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conta_id INTEGER NOT NULL,
    codigo_ativo VARCHAR(10) NOT NULL,
    tipo VARCHAR(10) NOT NULL,
    quantidade INTEGER NOT NULL,
    quantidade_executada INTEGER NOT NULL DEFAULT 0,
    preco REAL NOT NULL,
    preco_medio_execucao REAL,
    estado VARCHAR(30) NOT NULL,
    chave_idempotencia VARCHAR(100) NOT NULL UNIQUE,
    criada_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    atualizada_em DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conta_id)
        REFERENCES contas(id),

    FOREIGN KEY (codigo_ativo)
        REFERENCES ativos(codigo)
);

CREATE TABLE registros_auditoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ordem_id INTEGER,
    investidor_id INTEGER,
    evento VARCHAR(100) NOT NULL,
    resultado VARCHAR(255) NOT NULL,
    data_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (ordem_id)
        REFERENCES ordens(id),

    FOREIGN KEY (investidor_id)
        REFERENCES investidores(id)
);

CREATE INDEX idx_investidores_email
    ON investidores(email);

CREATE INDEX idx_ordens_chave_idempotencia
    ON ordens(chave_idempotencia);

CREATE INDEX idx_ordens_conta
    ON ordens(conta_id);

CREATE INDEX idx_auditoria_ordem
    ON registros_auditoria(ordem_id);

CREATE TRIGGER impedir_update_auditoria
BEFORE UPDATE ON registros_auditoria
BEGIN
    SELECT RAISE(
        ABORT,
        'Registros de auditoria são imutáveis'
    );
END;

CREATE TRIGGER impedir_delete_auditoria
BEFORE DELETE ON registros_auditoria
BEGIN
    SELECT RAISE(
        ABORT,
        'Registros de auditoria são imutáveis'
    );
END;