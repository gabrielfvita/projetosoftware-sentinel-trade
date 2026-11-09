import os

os.environ["MFA_TEST_CODE"] = "123456"

from fastapi.testclient import TestClient

from app.database.seed import popular_banco
from app.main import app


popular_banco()

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_com_sucesso():
    response = client.post(
        "/auth/login",
        json={
            "email": "gabriel@sentineltrade.com",
            "senha": "Sentinel123"
        }
    )

    assert response.status_code == 200
    assert response.json()["mfa_necessario"] is True


def test_login_invalido():
    response = client.post(
        "/auth/login",
        json={
            "email": "gabriel@sentineltrade.com",
            "senha": "SenhaErrada123"
        }
    )

    assert response.status_code == 401


def test_mfa_com_sucesso():
    response = client.post(
        "/auth/mfa",
        json={
            "investidor_id": 1,
            "codigo": "123456"
        }
    )

    assert response.status_code == 200
    assert response.json()["autenticado"] is True
    assert response.json()["access_token"]
    assert response.json()["conta_id"] > 0


def test_mfa_invalido():
    response = client.post(
        "/auth/mfa",
        json={
            "investidor_id": 1,
            "codigo": "000000"
        }
    )

    assert response.status_code == 401

def test_endpoint_protegido_exige_token():
    response = client.get("/carteiras/minha")
    assert response.status_code == 401


def test_endpoint_protegido_com_token():
    login = client.post("/auth/login", json={"email": "gabriel@sentineltrade.com", "senha": "Sentinel123"})
    mfa = client.post("/auth/mfa", json={"investidor_id": login.json()["investidor_id"], "codigo": "123456"})
    token = mfa.json()["access_token"]
    response = client.get("/carteiras/minha", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
