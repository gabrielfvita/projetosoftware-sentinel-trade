from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.conta_repository import ContaRepository
from app.repositories.investidor_repository import InvestidorRepository
from app.schemas.auth import LoginRequest, LoginResponse, MFARequest, MFAResponse
from app.security.session import criar_token, investidor_atual
from app.services.auditoria_service import AuditoriaService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


def criar_auth_service(db: Session) -> AuthService:
    return AuthService(InvestidorRepository(db), AuditoriaService(db))


@router.post("/login", response_model=LoginResponse)
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    try:
        investidor = criar_auth_service(db).autenticar_senha(str(dados.email).lower(), dados.senha)
    except ValueError as erro:
        raise HTTPException(status_code=401, detail=str(erro))
    return LoginResponse(
        mensagem="Senha validada. Informe o segundo fator.",
        mfa_necessario=investidor.mfa_habilitado,
        investidor_id=investidor.id,
    )


@router.post("/mfa", response_model=MFAResponse)
def validar_mfa(dados: MFARequest, db: Session = Depends(get_db)):
    service = criar_auth_service(db)
    try:
        service.validar_mfa(dados.investidor_id, dados.codigo)
    except ValueError as erro:
        raise HTTPException(status_code=401, detail=str(erro))

    conta = ContaRepository(db).buscar_primeira_por_investidor(dados.investidor_id)
    if conta is None:
        raise HTTPException(status_code=403, detail="Investidor não possui conta vinculada.")

    return MFAResponse(
        autenticado=True,
        mensagem="Autenticação concluída com sucesso.",
        access_token=criar_token(dados.investidor_id),
        investidor_id=dados.investidor_id,
        conta_id=conta.id,
    )


@router.get("/me")
def me(investidor=Depends(investidor_atual), db: Session = Depends(get_db)):
    conta = ContaRepository(db).buscar_primeira_por_investidor(investidor.id)
    return {
        "investidor_id": investidor.id,
        "nome": investidor.nome,
        "email": investidor.email,
        "conta_id": conta.id if conta else None,
    }
