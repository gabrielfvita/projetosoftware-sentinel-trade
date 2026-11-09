import pytest
from pydantic import ValidationError

from app.schemas.ordem import OrdemCreate
from app.security.mfa import MFAService
from app.services.duplicidade_service import DuplicidadeService


def test_codigo_ativo_valido():
    ordem = OrdemCreate(
        conta_id=1,
        codigo_ativo="petr4",
        tipo="compra",
        quantidade=10,
        preco=38.5,
        chave_idempotencia="ordem-000010"
    )

    assert ordem.codigo_ativo == "PETR4"


def test_codigo_ativo_com_caracteres_invalidos():
    with pytest.raises(ValidationError):
        OrdemCreate(
            conta_id=1,
            codigo_ativo="PETR4';DROP",
            tipo="compra",
            quantidade=10,
            preco=38.5,
            chave_idempotencia="ordem-000011"
        )


def test_quantidade_negativa():
    with pytest.raises(ValidationError):
        OrdemCreate(
            conta_id=1,
            codigo_ativo="PETR4",
            tipo="compra",
            quantidade=-10,
            preco=38.5,
            chave_idempotencia="ordem-000012"
        )


def test_quantidade_acima_do_limite():
    with pytest.raises(ValidationError):
        OrdemCreate(
            conta_id=1,
            codigo_ativo="PETR4",
            tipo="compra",
            quantidade=10001,
            preco=38.5,
            chave_idempotencia="ordem-000013"
        )


def test_chave_idempotencia_invalida():
    with pytest.raises(ValueError):
        DuplicidadeService.validar_chave(
            "abc!"
        )


def test_mfa_correto(monkeypatch):
    monkeypatch.setenv(
        "MFA_TEST_CODE",
        "123456"
    )

    assert MFAService.validar_codigo(
        "123456"
    )


def test_mfa_incorreto(monkeypatch):
    monkeypatch.setenv(
        "MFA_TEST_CODE",
        "123456"
    )

    assert not MFAService.validar_codigo(
        "000000"
    )