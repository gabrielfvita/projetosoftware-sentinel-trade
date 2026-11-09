import pytest

from app.domain.carteira import Carteira
from app.domain.conta import Conta
from app.domain.enums import TipoOrdem
from app.domain.ordem import Ordem
from app.services.validacao_service import ValidacaoService


def criar_conta(
    saldo: float = 50000,
    limite: float = 20000,
    situacao: str = "ativa"
) -> Conta:
    return Conta(
        id_conta=1,
        saldo_disponivel=saldo,
        limite_risco=limite,
        situacao=situacao
    )


def criar_carteira() -> Carteira:
    carteira = Carteira(id_carteira=1)

    carteira.adicionar_ativo(
        codigo_ativo="PETR4",
        quantidade=100
    )

    return carteira


def criar_ordem_compra(
    quantidade: int = 10,
    preco: float = 38.5
) -> Ordem:
    return Ordem(
        id_ordem=1,
        id_conta=1,
        codigo_ativo="PETR4",
        tipo=TipoOrdem.COMPRA,
        quantidade=quantidade,
        preco=preco
    )


def criar_ordem_venda(
    quantidade: int = 10,
    preco: float = 38.5
) -> Ordem:
    return Ordem(
        id_ordem=1,
        id_conta=1,
        codigo_ativo="PETR4",
        tipo=TipoOrdem.VENDA,
        quantidade=quantidade,
        preco=preco
    )


def test_compra_valida():
    service = ValidacaoService()

    service.validar_ordem(
        ordem=criar_ordem_compra(),
        conta=criar_conta(),
        carteira=criar_carteira()
    )


def test_saldo_insuficiente():
    service = ValidacaoService()

    conta = criar_conta(
        saldo=100,
        limite=100000
    )

    with pytest.raises(
        ValueError,
        match="Saldo insuficiente"
    ):
        service.validar_ordem(
            ordem=criar_ordem_compra(
                quantidade=10,
                preco=38.5
            ),
            conta=conta,
            carteira=criar_carteira()
        )


def test_limite_de_risco_excedido():
    service = ValidacaoService()

    conta = criar_conta(
        saldo=50000,
        limite=100
    )

    with pytest.raises(
        ValueError,
        match="limite de risco"
    ):
        service.validar_ordem(
            ordem=criar_ordem_compra(),
            conta=conta,
            carteira=criar_carteira()
        )


def test_venda_sem_posicao_suficiente():
    service = ValidacaoService()

    with pytest.raises(
        ValueError,
        match="Quantidade disponível insuficiente"
    ):
        service.validar_ordem(
            ordem=criar_ordem_venda(
                quantidade=150
            ),
            conta=criar_conta(),
            carteira=criar_carteira()
        )


def test_venda_de_ativo_inexistente():
    service = ValidacaoService()

    carteira = Carteira(
        id_carteira=1
    )

    with pytest.raises(
        ValueError,
        match="não existe na carteira"
    ):
        service.validar_ordem(
            ordem=criar_ordem_venda(),
            conta=criar_conta(),
            carteira=carteira
        )


def test_conta_bloqueada():
    service = ValidacaoService()

    with pytest.raises(
        ValueError,
        match="não está ativa"
    ):
        service.validar_ordem(
            ordem=criar_ordem_compra(),
            conta=criar_conta(
                situacao="bloqueada"
            ),
            carteira=criar_carteira()
        )