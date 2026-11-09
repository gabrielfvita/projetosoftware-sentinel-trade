from collections import deque
from enum import Enum

from app.domain.enums import TipoOrdem
from app.integrations.interfaces import BolsaInterface


class ResultadoBolsa(str, Enum):
    EXECUTADA = "executada"
    PARCIALMENTE_EXECUTADA = "parcialmente_executada"
    REJEITADA = "rejeitada"
    AGUARDANDO_PRECO = "aguardando_preco"


class ErroIntegracaoBolsa(Exception):
    pass


class BolsaSimulada(BolsaInterface):
    """Bolsa simulada para ordens limitadas.

    No fluxo normal, a cotacao de mercado decide se a ordem pode executar:
    - compra: executa quando cotacao <= preco limite;
    - venda: executa quando cotacao >= preco limite.

    Testes podem injetar resultados explicitos para exercitar execucao parcial,
    rejeicao e recuperacao sem depender de aleatoriedade.
    """

    def __init__(self, resultados=None, falhar=False):
        self._resultados = deque(resultados or [])
        self._falhar = falhar

    def processar_ordem(self, ordem=None, cotacao: float | None = None) -> ResultadoBolsa:
        if self._falhar:
            raise ErroIntegracaoBolsa("Falha simulada de comunicacao com a bolsa.")

        if self._resultados:
            return ResultadoBolsa(self._resultados.popleft())

        if ordem is None or cotacao is None:
            raise ErroIntegracaoBolsa("Ordem e cotacao sao obrigatorias para o processamento.")

        if cotacao <= 0:
            raise ErroIntegracaoBolsa("Cotacao de mercado invalida.")

        if ordem.tipo == TipoOrdem.COMPRA:
            return (
                ResultadoBolsa.EXECUTADA
                if cotacao <= ordem.preco
                else ResultadoBolsa.AGUARDANDO_PRECO
            )

        if ordem.tipo == TipoOrdem.VENDA:
            return (
                ResultadoBolsa.EXECUTADA
                if cotacao >= ordem.preco
                else ResultadoBolsa.AGUARDANDO_PRECO
            )

        return ResultadoBolsa.REJEITADA
