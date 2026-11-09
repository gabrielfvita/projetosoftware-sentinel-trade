from enum import Enum


class EstadoOrdem(str, Enum):
    CRIADA = "criada"
    VALIDADA = "validada"
    ENVIADA = "enviada"
    PARCIALMENTE_EXECUTADA = "parcialmente_executada"
    EXECUTADA = "executada"
    REJEITADA = "rejeitada"
    CANCELADA = "cancelada"


class TipoOrdem(str, Enum):
    COMPRA = "compra"
    VENDA = "venda"


class TipoAtivo(str, Enum):
    ACAO = "acao"
    ETF = "etf"
    FII = "fii"