from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator
)


class InvestidorCreate(BaseModel):
    nome: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    senha: str = Field(
        min_length=8,
        max_length=128
    )

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError(
                "Nome inválido."
            )

        return valor


class InvestidorUpdate(BaseModel):
    nome: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: EmailStr | None = None


class InvestidorResponse(BaseModel):
    id: int
    nome: str
    email: str
    status: str
    mfa_habilitado: bool