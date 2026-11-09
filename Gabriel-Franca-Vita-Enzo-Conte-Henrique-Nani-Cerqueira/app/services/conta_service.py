from app.repositories.conta_repository import (
    ContaRepository
)

from app.repositories.investidor_repository import (
    InvestidorRepository
)

from app.services.auditoria_service import (
    AuditoriaService
)


class ContaService:
    def __init__(
        self,
        conta_repository: ContaRepository,
        investidor_repository: InvestidorRepository,
        auditoria_service: AuditoriaService
    ):
        self._conta_repository = conta_repository
        self._investidor_repository = (
            investidor_repository
        )
        self._auditoria_service = (
            auditoria_service
        )

    def criar(
        self,
        investidor_id: int,
        saldo_inicial: float,
        limite_risco: float
    ):
        investidor = (
            self._investidor_repository.buscar_por_id(
                investidor_id
            )
        )

        if investidor is None:
            raise ValueError(
                "Investidor não encontrado."
            )

        if investidor.status != "ativo":
            raise ValueError(
                "Investidor não está ativo."
            )

        conta = self._conta_repository.criar(
            investidor_id=investidor_id,
            saldo_disponivel=saldo_inicial,
            limite_risco=limite_risco
        )

        self._auditoria_service.registrar(
            evento="CONTA_CRIADA",
            resultado="SUCESSO",
            investidor_id=investidor_id
        )

        return conta

    def consultar(
        self,
        conta_id: int
    ):
        conta = (
            self._conta_repository
            .buscar_model_por_id(
                conta_id
            )
        )

        if conta is None:
            raise ValueError(
                "Conta não encontrada."
            )

        return conta

    def listar_por_investidor(
        self,
        investidor_id: int
    ):
        investidor = (
            self._investidor_repository.buscar_por_id(
                investidor_id
            )
        )

        if investidor is None:
            raise ValueError(
                "Investidor não encontrado."
            )

        return (
            self._conta_repository
            .listar_por_investidor(
                investidor_id
            )
        )

    def atualizar_limite(
        self,
        conta_id: int,
        limite_risco: float
    ):
        conta = self.consultar(
            conta_id
        )

        conta.limite_risco = (
            limite_risco
        )

        conta = (
            self._conta_repository
            .atualizar_model(
                conta
            )
        )

        self._auditoria_service.registrar(
            evento="LIMITE_RISCO_ATUALIZADO",
            resultado="SUCESSO",
            investidor_id=conta.investidor_id
        )

        return conta

    def bloquear(
        self,
        conta_id: int
    ):
        conta = self.consultar(
            conta_id
        )

        conta.situacao = "bloqueada"

        conta = (
            self._conta_repository
            .atualizar_model(
                conta
            )
        )

        self._auditoria_service.registrar(
            evento="CONTA_BLOQUEADA",
            resultado="SUCESSO",
            investidor_id=conta.investidor_id
        )

        return conta

    def ativar(
        self,
        conta_id: int
    ):
        conta = self.consultar(
            conta_id
        )

        conta.situacao = "ativa"

        conta = (
            self._conta_repository
            .atualizar_model(
                conta
            )
        )

        self._auditoria_service.registrar(
            evento="CONTA_ATIVADA",
            resultado="SUCESSO",
            investidor_id=conta.investidor_id
        )

        return conta