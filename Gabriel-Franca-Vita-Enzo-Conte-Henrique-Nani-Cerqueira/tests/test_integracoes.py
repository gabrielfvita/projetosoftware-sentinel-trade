import pytest

from app.integrations.bolsa_simulada import (
    ErroIntegracaoBolsa
)


class BolsaComFalha:
    def processar_ordem(self):
        raise ErroIntegracaoBolsa(
            "Falha simulada."
        )


def test_falha_bolsa_controlada():
    bolsa = BolsaComFalha()

    with pytest.raises(
        ErroIntegracaoBolsa
    ):
        bolsa.processar_ordem()
from app.domain.enums import TipoOrdem
from app.domain.ordem import Ordem
from app.integrations.bolsa_simulada import BolsaSimulada, ResultadoBolsa


def _ordem_limite(tipo, preco):
    ordem = Ordem(1, 1, "PETR4", tipo, 10, preco)
    ordem.validar()
    ordem.enviar()
    return ordem


def test_compra_limite_executa_quando_cotacao_menor_ou_igual():
    ordem = _ordem_limite(TipoOrdem.COMPRA, 40.0)
    assert BolsaSimulada().processar_ordem(ordem, 38.5) == ResultadoBolsa.EXECUTADA


def test_compra_limite_aguarda_quando_cotacao_maior():
    ordem = _ordem_limite(TipoOrdem.COMPRA, 30.0)
    assert BolsaSimulada().processar_ordem(ordem, 38.5) == ResultadoBolsa.AGUARDANDO_PRECO


def test_venda_limite_executa_quando_cotacao_maior_ou_igual():
    ordem = _ordem_limite(TipoOrdem.VENDA, 35.0)
    assert BolsaSimulada().processar_ordem(ordem, 38.5) == ResultadoBolsa.EXECUTADA


def test_venda_limite_aguarda_quando_cotacao_menor():
    ordem = _ordem_limite(TipoOrdem.VENDA, 50.0)
    assert BolsaSimulada().processar_ordem(ordem, 38.5) == ResultadoBolsa.AGUARDANDO_PRECO
