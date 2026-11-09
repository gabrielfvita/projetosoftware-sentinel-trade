import pytest

from app.domain.enums import EstadoOrdem, TipoOrdem
from app.domain.ordem import Ordem


def criar_ordem() -> Ordem:
    return Ordem(
        id_ordem=1,
        id_conta=1,
        codigo_ativo="PETR4",
        tipo=TipoOrdem.COMPRA,
        quantidade=10,
        preco=38.5
    )


def test_ordem_inicia_como_criada():
    ordem = criar_ordem()

    assert ordem.estado == EstadoOrdem.CRIADA


def test_ordem_pode_ser_validada():
    ordem = criar_ordem()

    ordem.validar()

    assert ordem.estado == EstadoOrdem.VALIDADA


def test_ordem_pode_ser_enviada():
    ordem = criar_ordem()

    ordem.validar()
    ordem.enviar()

    assert ordem.estado == EstadoOrdem.ENVIADA


def test_ordem_pode_ser_executada():
    ordem = criar_ordem()

    ordem.validar()
    ordem.enviar()
    ordem.executar()

    assert ordem.estado == EstadoOrdem.EXECUTADA


def test_ordem_pode_ser_parcialmente_executada():
    ordem = criar_ordem()

    ordem.validar()
    ordem.enviar()
    ordem.executar_parcialmente()

    assert ordem.estado == EstadoOrdem.PARCIALMENTE_EXECUTADA


def test_ordem_parcial_pode_ser_finalizada():
    ordem = criar_ordem()

    ordem.validar()
    ordem.enviar()
    ordem.executar_parcialmente()
    ordem.executar()

    assert ordem.estado == EstadoOrdem.EXECUTADA


def test_nao_pode_executar_ordem_criada():
    ordem = criar_ordem()

    with pytest.raises(ValueError):
        ordem.executar()


def test_nao_pode_enviar_ordem_criada_sem_validacao():
    ordem = criar_ordem()

    with pytest.raises(ValueError):
        ordem.enviar()


def test_ordem_validada_pode_ser_cancelada():
    ordem = criar_ordem()

    ordem.validar()
    ordem.cancelar()

    assert ordem.estado == EstadoOrdem.CANCELADA


def test_nao_pode_cancelar_ordem_executada():
    ordem = criar_ordem()

    ordem.validar()
    ordem.enviar()
    ordem.executar()

    with pytest.raises(ValueError):
        ordem.cancelar()


def test_quantidade_invalida():
    with pytest.raises(ValueError):
        Ordem(
            id_ordem=1,
            id_conta=1,
            codigo_ativo="PETR4",
            tipo=TipoOrdem.COMPRA,
            quantidade=0,
            preco=38.5
        )


def test_preco_invalido():
    with pytest.raises(ValueError):
        Ordem(
            id_ordem=1,
            id_conta=1,
            codigo_ativo="PETR4",
            tipo=TipoOrdem.COMPRA,
            quantidade=10,
            preco=0
        )