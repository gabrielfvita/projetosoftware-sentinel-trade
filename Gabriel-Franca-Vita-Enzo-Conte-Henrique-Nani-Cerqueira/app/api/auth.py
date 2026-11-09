from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.repositories.investidor_repository import (
    InvestidorRepository
)

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    MFARequest,
    MFAResponse
)

from app.services.auditoria_service import (
    AuditoriaService
)

from app.services.auth_service import (
    AuthService
)


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


def criar_auth_service(
    db: Session
) -> AuthService:
    return AuthService(
        repository=InvestidorRepository(db),
        auditoria_service=AuditoriaService(db)
    )


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):
    service = criar_auth_service(db)

    try:
        investidor = service.autenticar_senha(
            email=str(dados.email).lower(),
            senha=dados.senha
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=401,
            detail=str(erro)
        )

    return LoginResponse(
        mensagem=(
            "Senha validada. "
            "Informe o segundo fator."
        ),
        mfa_necessario=investidor.mfa_habilitado,
        investidor_id=investidor.id
    )


@router.post(
    "/mfa",
    response_model=MFAResponse
)
def validar_mfa(
    dados: MFARequest,
    db: Session = Depends(get_db)
):
    service = criar_auth_service(db)

    try:
        service.validar_mfa(
            investidor_id=dados.investidor_id,
            codigo=dados.codigo
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=401,
            detail=str(erro)
        )

    return MFAResponse(
        autenticado=True,
        mensagem="Autenticação concluída com sucesso."
    )