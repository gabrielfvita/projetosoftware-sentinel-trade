from pydantic import BaseModel


class AtivoResponse(BaseModel):
    codigo: str
    nome: str
    tipo: str
    cotacao: float