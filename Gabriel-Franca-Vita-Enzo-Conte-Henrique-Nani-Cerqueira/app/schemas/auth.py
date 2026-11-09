import re
from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, valor: str) -> str:
        if not re.search(r"[A-Za-z]", valor) or not re.search(r"[0-9]", valor):
            raise ValueError("A senha deve conter letras e números.")
        return valor


class LoginResponse(BaseModel):
    mensagem: str
    mfa_necessario: bool
    investidor_id: int


class MFARequest(BaseModel):
    investidor_id: int = Field(gt=0)
    codigo: str = Field(min_length=6, max_length=6)

    @field_validator("codigo")
    @classmethod
    def validar_codigo(cls, valor: str) -> str:
        if not valor.isdigit():
            raise ValueError("O código MFA deve conter apenas números.")
        return valor


class MFAResponse(BaseModel):
    autenticado: bool
    mensagem: str
    access_token: str
    token_type: str = "bearer"
    investidor_id: int
    conta_id: int
