from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.repositories.conta_repository import (
    ContaRepository
)

from app.repositories.investidor_repository import (
    InvestidorRepository
)

from app.schemas.conta import (
    ContaCreate,
    ContaResponse,
    ContaUpdate
)

from app.services.auditoria_service import (
    AuditoriaService
)

from app.services.conta_service import (
    ContaService
)


router = APIRouter(
    prefix="/contas",
    tags=["Contas"]
)


def criar_service(
    db: Session
) -> ContaService:
    return ContaService(
        conta_repository=ContaRepository(db),
        investidor_repository=(
            InvestidorRepository(db)
        ),
        auditoria_service=AuditoriaService(db)
    )


def montar_response(
    conta
) -> ContaResponse:
    return ContaResponse(
        id=conta.id,
        investidor_id=conta.investidor_id,
        saldo_disponivel=conta.saldo_disponivel,
        limite_risco=conta.limite_risco,
        situacao=conta.situacao
    )


@router.post(
    "",
    response_model=ContaResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_conta(
    dados: ContaCreate,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        conta = service.criar(
            investidor_id=dados.investidor_id,
            saldo_inicial=dados.saldo_inicial,
            limite_risco=dados.limite_risco
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    return montar_response(
        conta
    )


@router.get(
    "/{conta_id}",
    response_model=ContaResponse
)
def consultar_conta(
    conta_id: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        conta = service.consultar(
            conta_id
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    return montar_response(
        conta
    )


@router.get(
    "/investidor/{investidor_id}",
    response_model=list[ContaResponse]
)
def listar_contas_investidor(
    investidor_id: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        contas = service.listar_por_investidor(
            investidor_id
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    return [
        montar_response(conta)
        for conta in contas
    ]


@router.patch(
    "/{conta_id}",
    response_model=ContaResponse
)
def atualizar_conta(
    conta_id: int,
    dados: ContaUpdate,
    db: Session = Depends(get_db)
):
    if dados.limite_risco is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "Nenhum campo válido "
                "foi informado."
            )
        )

    service = criar_service(db)

    try:
        conta = service.atualizar_limite(
            conta_id=conta_id,
            limite_risco=dados.limite_risco
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    return montar_response(
        conta
    )


@router.patch(
    "/{conta_id}/bloquear",
    response_model=ContaResponse
)
def bloquear_conta(
    conta_id: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        conta = service.bloquear(
            conta_id
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    return montar_response(
        conta
    )


@router.patch(
    "/{conta_id}/ativar",
    response_model=ContaResponse
)
def ativar_conta(
    conta_id: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        conta = service.ativar(
            conta_id
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    return montar_response(
        conta
    )