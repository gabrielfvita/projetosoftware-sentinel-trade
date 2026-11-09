import re
from pydantic import BaseModel, Field, field_validator
from app.domain.enums import TipoOrdem


class OrdemCreate(BaseModel):
    conta_id: int = Field(gt=0)
    codigo_ativo: str = Field(min_length=5, max_length=6)
    tipo: TipoOrdem
    quantidade: int = Field(gt=0, le=10000)
    preco: float = Field(gt=0, le=1_000_000, description="Preco limite da ordem")
    chave_idempotencia: str = Field(min_length=8, max_length=64)

    @field_validator("codigo_ativo")
    @classmethod
    def validar_codigo_ativo(cls, valor: str) -> str:
        valor = valor.strip().upper()
        if not re.fullmatch(r"[A-Z]{4}[0-9]{1,2}", valor):
            raise ValueError("Codigo de ativo invalido.")
        return valor

    @field_validator("chave_idempotencia")
    @classmethod
    def validar_chave_idempotencia(cls, valor: str) -> str:
        valor = valor.strip()
        if not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", valor):
            raise ValueError("Chave de idempotencia invalida.")
        return valor


class OrdemUpdate(BaseModel):
    quantidade: int | None = Field(default=None, gt=0, le=10000)
    preco: float | None = Field(default=None, gt=0, le=1_000_000, description="Preco limite da ordem")


class OrdemResponse(BaseModel):
    id_ordem: int
    conta_id: int
    codigo_ativo: str
    tipo: str
    quantidade: int
    quantidade_executada: int
    quantidade_remanescente: int
    preco: float
    preco_limite: float
    preco_medio_execucao: float | None
    estado: str
