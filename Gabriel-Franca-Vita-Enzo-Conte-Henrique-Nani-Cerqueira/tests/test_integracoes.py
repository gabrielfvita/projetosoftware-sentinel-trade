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