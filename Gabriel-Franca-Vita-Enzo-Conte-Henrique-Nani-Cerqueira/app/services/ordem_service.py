from app.domain.conta import Conta
from app.domain.carteira import Carteira
from app.domain.enums import TipoOrdem
from app.domain.ordem import Ordem

from app.integrations.bolsa_simulada import (
    BolsaSimulada,
    ResultadoBolsa,
    ErroIntegracaoBolsa
)

from app.integrations.notificacao_simulada import (
    NotificacaoSimulada
)

from app.repositories.carteira_repository import CarteiraRepository
from app.repositories.conta_repository import ContaRepository
from app.repositories.ordem_repository import OrdemRepository

from app.services.auditoria_service import AuditoriaService
from app.services.duplicidade_service import DuplicidadeService
from app.services.validacao_service import ValidacaoService


class OrdemService:
    def __init__(
        self,
        repository: OrdemRepository,
        validacao_service: ValidacaoService,
        auditoria_service: AuditoriaService,
        conta_repository: ContaRepository | None = None,
        carteira_repository: CarteiraRepository | None = None,
        bolsa: BolsaSimulada | None = None,
        notificacao: NotificacaoSimulada | None = None
    ):
        self._repository = repository
        self._validacao_service = validacao_service
        self._auditoria_service = auditoria_service
        self._conta_repository = conta_repository
        self._carteira_repository = carteira_repository

        self._bolsa = (
            bolsa
            if bolsa is not None
            else BolsaSimulada()
        )

        self._notificacao = (
            notificacao
            if notificacao is not None
            else NotificacaoSimulada()
        )

    def criar_ordem(
        self,
        ordem: Ordem,
        conta: Conta,
        carteira: Carteira,
        chave_idempotencia: str
    ) -> Ordem:
        chave = DuplicidadeService.validar_chave(
            chave_idempotencia
        )

        if self._repository.existe_chave_duplicidade(chave):
            self._auditoria_service.registrar(
                evento="ORDEM_DUPLICADA",
                resultado="REJEITADA"
            )

            raise ValueError(
                "Ordem duplicada detectada."
            )

        try:
            self._validacao_service.validar_ordem(
                ordem=ordem,
                conta=conta,
                carteira=carteira
            )

            ordem.validar()

            self._repository.salvar(
                ordem=ordem,
                chave_idempotencia=chave
            )

            self._auditoria_service.registrar(
                evento="ORDEM_CRIADA_E_VALIDADA",
                resultado="SUCESSO",
                ordem_id=ordem.id_ordem
            )

            return ordem

        except ValueError as erro:
            if ordem.estado.value == "criada":
                ordem.rejeitar()

            self._auditoria_service.registrar(
                evento="VALIDACAO_ORDEM",
                resultado=f"REJEITADA: {str(erro)}"
            )

            raise

    def consultar_ordem(
        self,
        id_ordem: int
    ) -> Ordem:
        ordem = self._repository.buscar_por_id(
            id_ordem
        )

        if ordem is None:
            raise ValueError(
                "Ordem não encontrada."
            )

        return ordem

    def atualizar_ordem(
        self,
        id_ordem: int,
        conta: Conta,
        carteira: Carteira,
        quantidade: int | None = None,
        preco: float | None = None
    ) -> Ordem:
        ordem = self.consultar_ordem(
            id_ordem
        )

        ordem.atualizar(
            quantidade=quantidade,
            preco=preco
        )

        self._validacao_service.validar_ordem(
            ordem=ordem,
            conta=conta,
            carteira=carteira
        )

        self._repository.atualizar(
            ordem
        )

        self._auditoria_service.registrar(
            evento="ORDEM_ATUALIZADA",
            resultado="SUCESSO",
            ordem_id=ordem.id_ordem
        )

        return ordem

    def cancelar_ordem(
        self,
        id_ordem: int
    ) -> Ordem:
        ordem = self.consultar_ordem(
            id_ordem
        )

        ordem.cancelar()

        self._repository.atualizar(
            ordem
        )

        self._auditoria_service.registrar(
            evento="ORDEM_CANCELADA",
            resultado="SUCESSO",
            ordem_id=ordem.id_ordem
        )

        self._notificacao.enviar(
            f"Ordem {ordem.id_ordem} cancelada."
        )

        return ordem

    def _aplicar_execucao(
        self,
        ordem: Ordem,
        quantidade_executada: int
    ) -> None:
        if self._conta_repository is None:
            raise ValueError(
                "Repositório de conta não configurado."
            )

        if self._carteira_repository is None:
            raise ValueError(
                "Repositório de carteira não configurado."
            )

        conta = self._conta_repository.buscar_por_id(
            ordem.id_conta
        )

        if conta is None:
            raise ValueError(
                "Conta não encontrada."
            )

        carteira = self._carteira_repository.buscar_por_conta(
            ordem.id_conta
        )

        valor_execucao = (
            quantidade_executada * ordem.preco
        )

        if ordem.tipo == TipoOrdem.COMPRA:
            conta.debitar(
                valor_execucao
            )

            carteira.adicionar_ativo(
                codigo_ativo=ordem.codigo_ativo,
                quantidade=quantidade_executada
            )

        elif ordem.tipo == TipoOrdem.VENDA:
            carteira.remover_ativo(
                codigo_ativo=ordem.codigo_ativo,
                quantidade=quantidade_executada
            )

            conta.creditar(
                valor_execucao
            )

        self._conta_repository.atualizar(
            conta
        )

        self._carteira_repository.atualizar(
            carteira
        )

    def processar_ordem(
        self,
        id_ordem: int
    ) -> Ordem:
        ordem = self.consultar_ordem(
            id_ordem
        )

        ordem.enviar()

        self._repository.atualizar(
            ordem
        )

        self._auditoria_service.registrar(
            evento="ORDEM_ENVIADA",
            resultado="SUCESSO",
            ordem_id=ordem.id_ordem
        )

        try:
            resultado = self._bolsa.processar_ordem()

        except ErroIntegracaoBolsa:
            self._auditoria_service.registrar(
                evento="FALHA_INTEGRACAO_BOLSA",
                resultado="PENDENTE_RECONCILIACAO",
                ordem_id=ordem.id_ordem
            )

            self._notificacao.enviar(
                (
                    f"Ordem {ordem.id_ordem} aguardando "
                    "reconciliação por falha de comunicação."
                )
            )

            raise ValueError(
                "Falha temporária na bolsa. "
                "A ordem permanece enviada e deverá ser reconciliada."
            )

        if resultado == ResultadoBolsa.EXECUTADA:
            self._aplicar_execucao(
                ordem=ordem,
                quantidade_executada=ordem.quantidade
            )

            ordem.executar()

        elif resultado == ResultadoBolsa.PARCIALMENTE_EXECUTADA:
            quantidade_parcial = max(
                1,
                ordem.quantidade // 2
            )

            self._aplicar_execucao(
                ordem=ordem,
                quantidade_executada=quantidade_parcial
            )

            ordem.executar_parcialmente()

        elif resultado == ResultadoBolsa.REJEITADA:
            ordem.rejeitar()

        self._repository.atualizar(
            ordem
        )

        self._auditoria_service.registrar(
            evento="RESULTADO_BOLSA",
            resultado=ordem.estado.value.upper(),
            ordem_id=ordem.id_ordem
        )

        self._notificacao.enviar(
            (
                f"Ordem {ordem.id_ordem}: "
                f"{ordem.estado.value}"
            )
        )

        return ordem

def reconciliar_ordem(
    self,
    id_ordem: int
) -> Ordem:
    ordem = self.consultar_ordem(
        id_ordem
    )

    if ordem.estado.value != "enviada":
        raise ValueError(
            "Apenas ordens enviadas podem ser reconciliadas."
        )

    try:
        resultado = self._bolsa.processar_ordem()

    except ErroIntegracaoBolsa:
        self._auditoria_service.registrar(
            evento="FALHA_RECONCILIACAO",
            resultado="PENDENTE_RECONCILIACAO",
            ordem_id=ordem.id_ordem
        )

        raise ValueError(
            "A reconciliação não pôde ser concluída. "
            "A ordem permanece enviada."
        )

    if resultado == ResultadoBolsa.EXECUTADA:
        self._aplicar_execucao(
            ordem=ordem,
            quantidade_executada=ordem.quantidade
        )

        ordem.executar()

    elif resultado == ResultadoBolsa.PARCIALMENTE_EXECUTADA:
        quantidade_parcial = max(
            1,
            ordem.quantidade // 2
        )

        self._aplicar_execucao(
            ordem=ordem,
            quantidade_executada=quantidade_parcial
        )

        ordem.executar_parcialmente()

    elif resultado == ResultadoBolsa.REJEITADA:
        ordem.rejeitar()

    self._repository.atualizar(
        ordem
    )

    self._auditoria_service.registrar(
        evento="ORDEM_RECONCILIADA",
        resultado=ordem.estado.value.upper(),
        ordem_id=ordem.id_ordem
    )

    self._notificacao.enviar(
        (
            f"Ordem {ordem.id_ordem} reconciliada: "
            f"{ordem.estado.value}"
        )
    )

    return ordem
    