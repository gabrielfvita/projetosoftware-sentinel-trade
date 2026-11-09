from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.repositories.investidor_repository import (
    InvestidorRepository
)

from app.schemas.investidor import (
    InvestidorCreate,
    InvestidorResponse,
    InvestidorUpdate
)

from app.services.auditoria_service import (
    AuditoriaService
)

from app.services.investidor_service import (
    InvestidorService
)


router = APIRouter(
    prefix="/investidores",
    tags=["Investidores"]
)


def criar_service(
    db: Session
) -> InvestidorService:
    return InvestidorService(
        repository=InvestidorRepository(db),
        auditoria_service=AuditoriaService(db)
    )


def montar_response(
    investidor
) -> InvestidorResponse:
    return InvestidorResponse(
        id=investidor.id,
        nome=investidor.nome,
        email=investidor.email,
        status=investidor.status,
        mfa_habilitado=investidor.mfa_habilitado
    )


@router.post(
    "",
    response_model=InvestidorResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_investidor(
    dados: InvestidorCreate,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        investidor = service.criar(
            nome=dados.nome,
            email=str(dados.email),
            senha=dados.senha
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    return montar_response(
        investidor
    )


@router.get(
    "",
    response_model=list[InvestidorResponse]
)
def listar_investidores(
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    return [
        montar_response(investidor)
        for investidor in service.listar()
    ]


@router.get(
    "/{investidor_id}",
    response_model=InvestidorResponse
)
def consultar_investidor(
    investidor_id: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        investidor = service.consultar(
            investidor_id
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    return montar_response(
        investidor
    )


@router.patch(
    "/{investidor_id}",
    response_model=InvestidorResponse
)
def atualizar_investidor(
    investidor_id: int,
    dados: InvestidorUpdate,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        investidor = service.atualizar(
            investidor_id=investidor_id,
            nome=dados.nome,
            email=(
                str(dados.email)
                if dados.email is not None
                else None
            )
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    return montar_response(
        investidor
    )


@router.patch(
    "/{investidor_id}/desativar",
    response_model=InvestidorResponse
)
def desativar_investidor(
    investidor_id: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        investidor = service.desativar(
            investidor_id
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    return montar_response(
        investidor
    )