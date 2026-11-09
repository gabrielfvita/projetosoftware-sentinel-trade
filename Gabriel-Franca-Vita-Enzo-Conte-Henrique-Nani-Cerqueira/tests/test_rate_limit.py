import pytest

from app.security.rate_limit import RateLimitService


def test_bloqueia_apos_cinco_tentativas():
    identificador = "teste@sentineltrade.com"

    RateLimitService.limpar(
        identificador
    )

    for _ in range(5):
        RateLimitService.verificar(
            identificador
        )

        RateLimitService.registrar_falha(
            identificador
        )

    with pytest.raises(
        ValueError,
        match="Muitas tentativas"
    ):
        RateLimitService.verificar(
            identificador
        )

    RateLimitService.limpar(
        identificador
    )


def test_limpar_tentativas():
    identificador = "teste2@sentineltrade.com"

    RateLimitService.registrar_falha(
        identificador
    )

    RateLimitService.limpar(
        identificador
    )

    RateLimitService.verificar(
        identificador
    )