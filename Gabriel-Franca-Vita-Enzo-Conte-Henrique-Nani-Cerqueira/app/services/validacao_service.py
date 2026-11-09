from app.domain.conta import Conta
from app.domain.carteira import Carteira
from app.domain.ordem import Ordem
from app.domain.enums import TipoOrdem


class ValidacaoService:
    def validar_ordem(
        self,
        ordem: Ordem,
        conta: Conta,
        carteira: Carteira
    ) -> None:
        self._validar_conta_ativa(conta)
        self._validar_limite_risco(ordem, conta)

        if ordem.tipo == TipoOrdem.COMPRA:
            self._validar_saldo(ordem, conta)

        elif ordem.tipo == TipoOrdem.VENDA:
            self._validar_posicao(ordem, carteira)

        else:
            raise ValueError("Tipo de ordem inválido.")

    def _validar_conta_ativa(self, conta: Conta) -> None:
        if conta.situacao != "ativa":
            raise ValueError("A conta não está ativa.")

    def _validar_saldo(
        self,
        ordem: Ordem,
        conta: Conta
    ) -> None:
        valor_total = ordem.quantidade * ordem.preco

        if valor_total > conta.saldo_disponivel:
            raise ValueError("Saldo insuficiente para realizar a compra.")

    def _validar_posicao(
        self,
        ordem: Ordem,
        carteira: Carteira
    ) -> None:
        posicao = carteira.consultar_posicao(ordem.codigo_ativo)

        if posicao is None:
            raise ValueError("O ativo não existe na carteira.")

        if ordem.quantidade > posicao.quantidade_disponivel:
            raise ValueError(
                "Quantidade disponível insuficiente para realizar a venda."
            )

    def _validar_limite_risco(
        self,
        ordem: Ordem,
        conta: Conta
    ) -> None:
        valor_total = ordem.quantidade * ordem.preco

        if valor_total > conta.limite_risco:
            raise ValueError("A ordem excede o limite de risco da conta.")