from enum import Enum
from secrets import choice

from app.integrations.interfaces import BolsaInterface


class ResultadoBolsa(str, Enum):
    EXECUTADA = "executada"
    PARCIALMENTE_EXECUTADA = "parcialmente_executada"
    REJEITADA = "rejeitada"


class ErroIntegracaoBolsa(Exception):
    pass


class BolsaSimulada(BolsaInterface):

    def processar_ordem(
        self
    ) -> ResultadoBolsa:
        try:
            return choice(
                [
                    ResultadoBolsa.EXECUTADA,
                    ResultadoBolsa.PARCIALMENTE_EXECUTADA,
                    ResultadoBolsa.REJEITADA
                ]
            )

        except Exception as erro:
            raise ErroIntegracaoBolsa(
                "Falha ao processar ordem na bolsa simulada."
            ) from erro