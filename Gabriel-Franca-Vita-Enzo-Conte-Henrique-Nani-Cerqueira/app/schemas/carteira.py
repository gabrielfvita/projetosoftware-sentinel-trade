from pydantic import BaseModel


class PosicaoResponse(BaseModel):
    codigo_ativo: str
    quantidade: int
    quantidade_disponivel: int


class CarteiraResponse(BaseModel):
    conta_id: int
    saldo_disponivel: float
    limite_risco: float
    situacao: str
    posicoes: list[PosicaoResponse]