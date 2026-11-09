from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.repositories.auditoria_repository import (
    AuditoriaRepository
)

from app.repositories.conta_repository import (
    ContaRepository
)

from app.repositories.ordem_repository import (
    OrdemRepository
)

from app.schemas.historico import (
    AuditoriaResponse,
    HistoricoOrdemResponse
)

from app.services.historico_service import (
    HistoricoService
)


router = APIRouter(
    prefix="/historico",
    tags=["Histórico"]
)


def criar_service(
    db: Session
) -> HistoricoService:
    return HistoricoService(
        ordem_repository=OrdemRepository(db),
        conta_repository=ContaRepository(db),
        auditoria_repository=AuditoriaRepository(db)
    )


@router.get(
    "/contas/{conta_id}/ordens",
    response_model=list[HistoricoOrdemResponse]
)
def consultar_historico_ordens(
    conta_id: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        ordens = service.listar_ordens_conta(
            conta_id
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    return [
        HistoricoOrdemResponse(
            id_ordem=ordem.id_ordem,
            conta_id=ordem.id_conta,
            codigo_ativo=ordem.codigo_ativo,
            tipo=ordem.tipo.value,
            quantidade=ordem.quantidade,
            preco=ordem.preco,
            estado=ordem.estado.value
        )
        for ordem in ordens
    ]


@router.get(
    "/ordens/{ordem_id}/auditoria",
    response_model=list[AuditoriaResponse]
)
def consultar_auditoria_ordem(
    ordem_id: int,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        registros = service.listar_auditoria_ordem(
            ordem_id
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    return [
        AuditoriaResponse(
            id=registro.id,
            ordem_id=registro.ordem_id,
            investidor_id=registro.investidor_id,
            evento=registro.evento,
            resultado=registro.resultado,
            data_hora=registro.data_hora
        )
        for registro in registros
    ]