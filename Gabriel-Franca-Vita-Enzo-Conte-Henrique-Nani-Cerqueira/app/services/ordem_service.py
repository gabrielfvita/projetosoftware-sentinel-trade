from app.domain.conta import Conta
from app.domain.carteira import Carteira
from app.domain.enums import EstadoOrdem, TipoOrdem
from app.domain.ordem import Ordem
from app.integrations.bolsa_simulada import BolsaSimulada, ErroIntegracaoBolsa, ResultadoBolsa
from app.integrations.cotacao_simulada import CotacaoSimulada, ErroIntegracaoCotacao
from app.integrations.notificacao_simulada import ErroNotificacao, NotificacaoSimulada
from app.repositories.ativo_repository import AtivoRepository
from app.repositories.carteira_repository import CarteiraRepository
from app.repositories.conta_repository import ContaRepository
from app.repositories.ordem_repository import OrdemRepository
from app.services.auditoria_service import AuditoriaService
from app.services.duplicidade_service import DuplicidadeService
from app.services.validacao_service import ValidacaoService


class OrdemService:
    def __init__(self, repository: OrdemRepository, validacao_service: ValidacaoService,
                 auditoria_service: AuditoriaService, conta_repository: ContaRepository | None = None,
                 carteira_repository: CarteiraRepository | None = None,
                 ativo_repository: AtivoRepository | None = None,
                 cotacao_service: CotacaoSimulada | None = None,
                 bolsa: BolsaSimulada | None = None,
                 notificacao: NotificacaoSimulada | None = None):
        self._repository = repository
        self._validacao_service = validacao_service
        self._auditoria_service = auditoria_service
        self._conta_repository = conta_repository
        self._carteira_repository = carteira_repository
        self._ativo_repository = ativo_repository
        self._cotacao_service = cotacao_service if cotacao_service is not None else CotacaoSimulada()
        self._bolsa = bolsa if bolsa is not None else BolsaSimulada()
        self._notificacao = notificacao if notificacao is not None else NotificacaoSimulada()

    def _investidor_id(self, ordem: Ordem) -> int | None:
        if self._conta_repository is None:
            return None
        return self._conta_repository.buscar_investidor_id(ordem.id_conta)

    def _notificar(self, ordem: Ordem, mensagem: str) -> None:
        investidor_id = self._investidor_id(ordem)
        destinatario = f"investidor:{investidor_id}" if investidor_id else "investidor:desconhecido"
        try:
            self._notificacao.enviar(destinatario, mensagem)
        except ErroNotificacao as erro:
            self._auditoria_service.registrar(
                evento="FALHA_NOTIFICACAO",
                resultado=str(erro),
                ordem_id=ordem.id_ordem,
                investidor_id=investidor_id,
            )

    def _consultar_cotacao(self, ordem: Ordem) -> float:
        if self._ativo_repository is None:
            raise ValueError("Repositorio de ativos nao configurado.")
        ativo = self._ativo_repository.buscar_por_codigo(ordem.codigo_ativo)
        if ativo is None:
            raise ValueError("Ativo nao encontrado.")
        try:
            return self._cotacao_service.consultar(ativo)
        except ErroIntegracaoCotacao as erro:
            raise ValueError("Nao foi possivel consultar a cotacao de mercado.") from erro

    def criar_ordem(self, ordem: Ordem, conta: Conta, carteira: Carteira, chave_idempotencia: str) -> Ordem:
        chave = DuplicidadeService.validar_chave(chave_idempotencia)
        if self._repository.existe_chave_duplicidade(chave):
            self._auditoria_service.registrar(evento="ORDEM_DUPLICADA", resultado="REJEITADA")
            raise ValueError("Ordem duplicada detectada.")

        try:
            self._validacao_service.validar_ordem(ordem=ordem, conta=conta, carteira=carteira)
            ordem.validar()
        except ValueError as erro:
            if ordem.estado == EstadoOrdem.CRIADA:
                ordem.rejeitar()
            self._auditoria_service.registrar(evento="VALIDACAO_ORDEM", resultado=f"REJEITADA: {erro}")
            raise

        self._repository.salvar(ordem=ordem, chave_idempotencia=chave)
        self._auditoria_service.registrar(
            evento="ORDEM_CRIADA_E_VALIDADA", resultado="SUCESSO",
            ordem_id=ordem.id_ordem, investidor_id=self._investidor_id(ordem)
        )
        return self.processar_ordem(ordem.id_ordem)

    def consultar_ordem(self, id_ordem: int) -> Ordem:
        ordem = self._repository.buscar_por_id(id_ordem)
        if ordem is None:
            raise ValueError("Ordem nao encontrada.")
        return ordem

    def atualizar_ordem(self, id_ordem: int, conta: Conta, carteira: Carteira,
                        quantidade: int | None = None, preco: float | None = None) -> Ordem:
        ordem = self.consultar_ordem(id_ordem)
        ordem.atualizar(quantidade=quantidade, preco=preco)
        self._validacao_service.validar_ordem(ordem=ordem, conta=conta, carteira=carteira)
        self._repository.atualizar(ordem)
        self._auditoria_service.registrar(
            evento="ORDEM_ATUALIZADA", resultado="SUCESSO",
            ordem_id=ordem.id_ordem, investidor_id=self._investidor_id(ordem)
        )
        return ordem

    def cancelar_ordem(self, id_ordem: int) -> Ordem:
        ordem = self.consultar_ordem(id_ordem)
        ordem.cancelar()
        self._repository.atualizar(ordem)
        self._auditoria_service.registrar(
            evento="ORDEM_CANCELADA", resultado="SUCESSO",
            ordem_id=ordem.id_ordem, investidor_id=self._investidor_id(ordem)
        )
        self._notificar(ordem, f"Ordem {ordem.id_ordem} cancelada. Quantidade remanescente: {ordem.quantidade_remanescente}.")
        return ordem

    def _aplicar_execucao(self, ordem: Ordem, quantidade_executada: int, preco_execucao: float) -> None:
        if self._conta_repository is None or self._carteira_repository is None:
            raise ValueError("Repositorios financeiros nao configurados.")
        conta = self._conta_repository.buscar_por_id(ordem.id_conta)
        if conta is None:
            raise ValueError("Conta nao encontrada.")
        carteira = self._carteira_repository.buscar_por_conta(ordem.id_conta)
        valor = quantidade_executada * preco_execucao
        if ordem.tipo == TipoOrdem.COMPRA:
            conta.debitar(valor)
            carteira.adicionar_ativo(ordem.codigo_ativo, quantidade_executada)
        else:
            carteira.remover_ativo(ordem.codigo_ativo, quantidade_executada)
            conta.creditar(valor)
        self._conta_repository.atualizar(conta)
        self._carteira_repository.atualizar(carteira)

    def _aplicar_resultado(self, ordem: Ordem, resultado: ResultadoBolsa, cotacao: float) -> Ordem:
        restante = ordem.quantidade_remanescente
        if resultado == ResultadoBolsa.EXECUTADA:
            self._aplicar_execucao(ordem, restante, cotacao)
            ordem.executar(cotacao)
        elif resultado == ResultadoBolsa.PARCIALMENTE_EXECUTADA:
            if restante <= 1:
                self._aplicar_execucao(ordem, restante, cotacao)
                ordem.executar(cotacao)
            else:
                quantidade_parcial = max(1, restante // 2)
                if quantidade_parcial >= restante:
                    quantidade_parcial = restante - 1
                self._aplicar_execucao(ordem, quantidade_parcial, cotacao)
                ordem.executar_parcialmente(quantidade_parcial, cotacao)
        elif resultado == ResultadoBolsa.REJEITADA:
            ordem.rejeitar()
        elif resultado == ResultadoBolsa.AGUARDANDO_PRECO:
            pass
        self._repository.atualizar(ordem)
        return ordem

    def processar_ordem(self, id_ordem: int) -> Ordem:
        ordem = self.consultar_ordem(id_ordem)
        if ordem.estado == EstadoOrdem.VALIDADA:
            ordem.enviar()
            self._repository.atualizar(ordem)
            self._auditoria_service.registrar(
                evento="ORDEM_ENVIADA", resultado="SUCESSO",
                ordem_id=ordem.id_ordem, investidor_id=self._investidor_id(ordem)
            )
        elif ordem.estado not in {EstadoOrdem.ENVIADA, EstadoOrdem.PARCIALMENTE_EXECUTADA}:
            raise ValueError("A ordem nao esta em estado processavel.")

        cotacao = self._consultar_cotacao(ordem)
        try:
            resultado = self._bolsa.processar_ordem(ordem, cotacao)
        except ErroIntegracaoBolsa:
            self._auditoria_service.registrar(
                evento="FALHA_INTEGRACAO_BOLSA", resultado="PENDENTE_RECONCILIACAO",
                ordem_id=ordem.id_ordem, investidor_id=self._investidor_id(ordem)
            )
            self._notificar(ordem, f"Ordem {ordem.id_ordem} aguardando reconciliacao por falha de comunicacao.")
            raise ValueError("Falha temporaria na bolsa. A ordem permanece enviada e devera ser reconciliada.")

        ordem = self._aplicar_resultado(ordem, resultado, cotacao)

        if resultado == ResultadoBolsa.AGUARDANDO_PRECO:
            self._auditoria_service.registrar(
                evento="ORDEM_AGUARDANDO_PRECO",
                resultado=f"COTACAO={cotacao:.2f};LIMITE={ordem.preco:.2f}",
                ordem_id=ordem.id_ordem, investidor_id=self._investidor_id(ordem)
            )
            self._notificar(
                ordem,
                f"Ordem {ordem.id_ordem} enviada e aguardando condicao de preco. "
                f"Cotacao: {cotacao:.2f}; limite: {ordem.preco:.2f}."
            )
            return ordem

        self._auditoria_service.registrar(
            evento="RESULTADO_BOLSA",
            resultado=f"{ordem.estado.value.upper()};COTACAO={cotacao:.2f}",
            ordem_id=ordem.id_ordem, investidor_id=self._investidor_id(ordem)
        )
        self._notificar(
            ordem,
            f"Ordem {ordem.id_ordem}: {ordem.estado.value}. "
            f"Executado: {ordem.quantidade_executada}/{ordem.quantidade}. "
            f"Preco medio: {ordem.preco_medio_execucao or 0:.2f}."
        )
        return ordem

    def reconciliar_ordem(self, id_ordem: int) -> Ordem:
        ordem = self.consultar_ordem(id_ordem)
        if ordem.estado not in {EstadoOrdem.ENVIADA, EstadoOrdem.PARCIALMENTE_EXECUTADA}:
            raise ValueError("Apenas ordens enviadas ou parcialmente executadas podem ser reconciliadas.")
        return self.processar_ordem(id_ordem)
