from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.domain.ordem import Ordem

from app.repositories.ativo_repository import AtivoRepository
from app.repositories.carteira_repository import CarteiraRepository
from app.repositories.conta_repository import ContaRepository
from app.repositories.ordem_repository import OrdemRepository

from app.schemas.ordem import (
    OrdemCreate,
    OrdemResponse,
    OrdemUpdate
)

from app.services.auditoria_service import AuditoriaService
from app.services.ordem_service import OrdemService
from app.services.validacao_service import ValidacaoService


router = APIRouter(
    prefix="/ordens",
    tags=["Ordens"]
)


def criar_service(
    db: Session
) -> OrdemService:
    return OrdemService(
        repository=OrdemRepository(db),
        validacao_service=ValidacaoService(),
        auditoria_service=AuditoriaService(db),
        conta_repository=ContaRepository(db),
        carteira_repository=CarteiraRepository(db)
    )


def montar_response(
    ordem: Ordem
) -> OrdemResponse:
    return OrdemResponse(
        id_ordem=ordem.id_ordem,
        conta_id=ordem.id_conta,
        codigo_ativo=ordem.codigo_ativo,
        tipo=ordem.tipo.value,
        quantidade=ordem.quantidade,
        preco=ordem.preco,
        estado=ordem.estado.value
    )


@router.post(
    "",
    response_model=OrdemResponse,
    status_code=status.HTTP_201_CREATED
)
def criar_ordem(
    dados: OrdemCreate,
    db: Session = Depends(get_db)
):
    conta_repository = ContaRepository(db)
    carteira_repository = CarteiraRepository(db)
    ativo_repository = AtivoRepository(db)

    conta = conta_repository.buscar_por_id(
        dados.conta_id
    )

    if conta is None:
        raise HTTPException(
            status_code=404,
            detail="Conta não encontrada."
        )

    ativo = ativo_repository.buscar_por_codigo(
        dados.codigo_ativo
    )

    if ativo is None:
        raise HTTPException(
            status_code=404,
            detail="Ativo não encontrado."
        )

    carteira = carteira_repository.buscar_por_conta(
        dados.conta_id
    )

    ordem = Ordem(
        id_ordem=None,
        id_conta=dados.conta_id,
        codigo_ativo=dados.codigo_ativo,
        tipo=dados.tipo,
        quantidade=dados.quantidade,
        preco=dados.preco
    )

    service = criar_service(db)

    try:
        ordem = service.criar_ordem(
            ordem=ordem,
            conta=conta,
            carteira=carteira,
            chave_idempotencia=dados.chave_idempotencia
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    return montar_response(ordem)


@router.get(
    "/{id_ordem}",
    response_model=OrdemResponse
)
def consultar_ordem(
    id_ordem: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        ordem = service.consultar_ordem(
            id_ordem
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    return montar_response(ordem)


@router.patch(
    "/{id_ordem}",
    response_model=OrdemResponse
)
def atualizar_ordem(
    id_ordem: int,
    dados: OrdemUpdate,
    db: Session = Depends(get_db)
):
    repository = OrdemRepository(db)

    ordem_existente = repository.buscar_por_id(
        id_ordem
    )

    if ordem_existente is None:
        raise HTTPException(
            status_code=404,
            detail="Ordem não encontrada."
        )

    conta_repository = ContaRepository(db)
    carteira_repository = CarteiraRepository(db)

    conta = conta_repository.buscar_por_id(
        ordem_existente.id_conta
    )

    if conta is None:
        raise HTTPException(
            status_code=404,
            detail="Conta não encontrada."
        )

    carteira = carteira_repository.buscar_por_conta(
        ordem_existente.id_conta
    )

    service = criar_service(db)

    try:
        ordem = service.atualizar_ordem(
            id_ordem=id_ordem,
            conta=conta,
            carteira=carteira,
            quantidade=dados.quantidade,
            preco=dados.preco
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    return montar_response(ordem)


@router.patch(
    "/{id_ordem}/cancelar",
    response_model=OrdemResponse
)
def cancelar_ordem(
    id_ordem: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        ordem = service.cancelar_ordem(
            id_ordem
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    return montar_response(ordem)


@router.post(
    "/{id_ordem}/processar",
    response_model=OrdemResponse
)
def processar_ordem(
    id_ordem: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        ordem = service.processar_ordem(
            id_ordem
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    return montar_response(ordem)

@router.post(
    "/{id_ordem}/reconciliar",
    response_model=OrdemResponse
)
def reconciliar_ordem(
    id_ordem: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        ordem = service.reconciliar_ordem(
            id_ordem
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=400,
            detail=str(erro)
        )

    return montar_response(
        ordem
    )