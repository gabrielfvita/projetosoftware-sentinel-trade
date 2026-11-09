from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint
)

from app.database.database import Base


class InvestidorModel(Base):
    __tablename__ = "investidores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)
    mfa_habilitado = Column(Boolean, nullable=False, default=True)
    status = Column(String(20), nullable=False, default="ativo")


class ContaModel(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)

    investidor_id = Column(
        Integer,
        ForeignKey("investidores.id"),
        nullable=False
    )

    saldo_disponivel = Column(Float, nullable=False, default=0)
    limite_risco = Column(Float, nullable=False)
    situacao = Column(String(20), nullable=False, default="ativa")


class AtivoModel(Base):
    __tablename__ = "ativos"

    codigo = Column(String(10), primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(20), nullable=False)
    cotacao = Column(Float, nullable=False)


class PosicaoCarteiraModel(Base):
    __tablename__ = "posicoes_carteira"

    id = Column(Integer, primary_key=True, index=True)

    conta_id = Column(
        Integer,
        ForeignKey("contas.id"),
        nullable=False
    )

    codigo_ativo = Column(
        String(10),
        ForeignKey("ativos.codigo"),
        nullable=False
    )

    quantidade = Column(Integer, nullable=False, default=0)
    quantidade_disponivel = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        UniqueConstraint(
            "conta_id",
            "codigo_ativo",
            name="uq_posicao_conta_ativo"
        ),
    )


class OrdemModel(Base):
    __tablename__ = "ordens"

    id = Column(Integer, primary_key=True, index=True)

    conta_id = Column(
        Integer,
        ForeignKey("contas.id"),
        nullable=False
    )

    codigo_ativo = Column(
        String(10),
        ForeignKey("ativos.codigo"),
        nullable=False
    )

    tipo = Column(String(10), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    estado = Column(String(30), nullable=False)

    chave_idempotencia = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )

    criada_em = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    atualizada_em = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class RegistroAuditoriaModel(Base):
    __tablename__ = "registros_auditoria"

    id = Column(Integer, primary_key=True, index=True)

    ordem_id = Column(
        Integer,
        ForeignKey("ordens.id"),
        nullable=True
    )

    investidor_id = Column(
        Integer,
        ForeignKey("investidores.id"),
        nullable=True
    )

    evento = Column(String(100), nullable=False)
    resultado = Column(String(50), nullable=False)

    data_hora = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )