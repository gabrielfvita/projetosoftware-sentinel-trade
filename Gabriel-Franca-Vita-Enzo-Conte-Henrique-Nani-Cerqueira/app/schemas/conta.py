from pydantic import BaseModel, Field


class ContaCreate(BaseModel):
    investidor_id: int = Field(gt=0)

    saldo_inicial: float = Field(
        default=0,
        ge=0,
        le=100_000_000
    )

    limite_risco: float = Field(
        gt=0,
        le=100_000_000
    )


class ContaUpdate(BaseModel):
    limite_risco: float | None = Field(
        default=None,
        gt=0,
        le=100_000_000
    )


class ContaResponse(BaseModel):
    id: int
    investidor_id: int
    saldo_disponivel: float
    limite_risco: float
    situacao: str