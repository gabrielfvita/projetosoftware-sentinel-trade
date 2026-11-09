import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.investidor_repository import InvestidorRepository

_bearer = HTTPBearer(auto_error=False)
_process_secret = secrets.token_urlsafe(48)


def _secret() -> bytes:
    return os.getenv("SESSION_SECRET", _process_secret).encode("utf-8")


def criar_token(investidor_id: int, duracao_segundos: int = 8 * 60 * 60) -> str:
    payload = {
        "investidor_id": investidor_id,
        "exp": int(time.time()) + duracao_segundos,
    }
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    encoded = base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")
    assinatura = hmac.new(_secret(), encoded.encode("ascii"), hashlib.sha256).hexdigest()
    return f"{encoded}.{assinatura}"


def validar_token(token: str) -> int:
    try:
        encoded, assinatura = token.rsplit(".", 1)
        esperada = hmac.new(_secret(), encoded.encode("ascii"), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(assinatura, esperada):
            raise ValueError
        padded = encoded + "=" * (-len(encoded) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
        if int(payload["exp"]) < int(time.time()):
            raise ValueError
        return int(payload["investidor_id"])
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        raise HTTPException(status_code=401, detail="Sessão inválida ou expirada.")


def investidor_atual(
    credenciais: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
):
    if credenciais is None or credenciais.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Autenticação necessária.")

    investidor_id = validar_token(credenciais.credentials)
    investidor = InvestidorRepository(db).buscar_por_id(investidor_id)

    if investidor is None or investidor.status != "ativo":
        raise HTTPException(status_code=401, detail="Sessão inválida.")

    return investidor


def exigir_conta_do_investidor(db: Session, conta_id: int, investidor_id: int):
    from app.repositories.conta_repository import ContaRepository

    model = ContaRepository(db).buscar_model_por_id(conta_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")
    if model.investidor_id != investidor_id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado a esta conta.")
    return model
