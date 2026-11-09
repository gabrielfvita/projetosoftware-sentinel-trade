import time

from app.domain.ativo import Ativo
from app.integrations.interfaces import CotacaoInterface


class ErroIntegracaoCotacao(Exception):
    pass


class CotacaoSimulada(CotacaoInterface):

    def consultar(
        self,
        ativo: Ativo,
        timeout_segundos: float = 2.0
    ) -> float:
        inicio = time.monotonic()

        try:
            cotacao = ativo.cotacao

            if cotacao <= 0:
                raise ValueError(
                    "Cotação recebida é inválida."
                )

        except Exception as erro:
            raise ErroIntegracaoCotacao(
                "Falha ao consultar cotação externa."
            ) from erro

        if time.monotonic() - inicio > timeout_segundos:
            raise ErroIntegracaoCotacao(
                "Timeout ao consultar cotação externa."
            )

        return cotacao