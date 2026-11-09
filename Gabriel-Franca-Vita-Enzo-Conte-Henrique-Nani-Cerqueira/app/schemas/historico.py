from datetime import datetime

from pydantic import BaseModel


class HistoricoOrdemResponse(BaseModel):
    id_ordem: int
    conta_id: int
    codigo_ativo: str
    tipo: str
    quantidade: int
    preco: float
    estado: str


class AuditoriaResponse(BaseModel):
    id: int
    ordem_id: int | None
    investidor_id: int | None
    evento: str
    resultado: str
    data_hora: datetime