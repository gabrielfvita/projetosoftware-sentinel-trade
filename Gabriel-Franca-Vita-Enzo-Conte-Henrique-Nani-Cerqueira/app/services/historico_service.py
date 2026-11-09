from app.repositories.auditoria_repository import (
    AuditoriaRepository
)

from app.repositories.conta_repository import (
    ContaRepository
)

from app.repositories.ordem_repository import (
    OrdemRepository
)


class HistoricoService:
    def __init__(
        self,
        ordem_repository: OrdemRepository,
        conta_repository: ContaRepository,
        auditoria_repository: AuditoriaRepository
    ):
        self._ordem_repository = ordem_repository
        self._conta_repository = conta_repository
        self._auditoria_repository = auditoria_repository

    def listar_ordens_conta(
        self,
        conta_id: int
    ):
        conta = self._conta_repository.buscar_por_id(
            conta_id
        )

        if conta is None:
            raise ValueError(
                "Conta não encontrada."
            )

        return self._ordem_repository.listar_por_conta(
            conta_id
        )

    def listar_auditoria_ordem(
        self,
        ordem_id: int
    ):
        ordem = self._ordem_repository.buscar_por_id(
            ordem_id
        )

        if ordem is None:
            raise ValueError(
                "Ordem não encontrada."
            )

        return self._auditoria_repository.listar_por_ordem(
            ordem_id
        )