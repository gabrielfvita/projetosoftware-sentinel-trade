from app.integrations.cotacao_simulada import (
    CotacaoSimulada,
    ErroIntegracaoCotacao
)

from app.repositories.ativo_repository import (
    AtivoRepository
)


class AtivoService:
    def __init__(
        self,
        repository: AtivoRepository,
        cotacao_service: CotacaoSimulada
    ):
        self._repository = repository
        self._cotacao_service = cotacao_service

    def listar(self):
        return self._repository.listar()

    def consultar(
        self,
        codigo: str
    ):
        ativo = self._repository.buscar_por_codigo(
            codigo
        )

        if ativo is None:
            raise ValueError(
                "Ativo não encontrado."
            )

        return ativo

    def consultar_cotacao(
        self,
        codigo: str
    ) -> float:
        ativo = self.consultar(
            codigo
        )

        try:
            return self._cotacao_service.consultar(
                ativo
            )

        except ErroIntegracaoCotacao as erro:
            raise ValueError(
                "Não foi possível consultar a cotação."
            ) from erro