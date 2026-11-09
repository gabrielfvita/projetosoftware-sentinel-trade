from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.integrations.cotacao_simulada import (
    CotacaoSimulada
)

from app.repositories.ativo_repository import (
    AtivoRepository
)

from app.schemas.ativo import (
    AtivoResponse
)

from app.services.ativo_service import (
    AtivoService
)


router = APIRouter(
    prefix="/ativos",
    tags=["Ativos"]
)


def criar_service(
    db: Session
) -> AtivoService:
    return AtivoService(
        repository=AtivoRepository(db),
        cotacao_service=CotacaoSimulada()
    )


def montar_response(
    ativo,
    cotacao: float
) -> AtivoResponse:
    return AtivoResponse(
        codigo=ativo.codigo,
        nome=ativo.nome,
        tipo=ativo.tipo.value,
        cotacao=cotacao
    )


@router.get(
    "",
    response_model=list[AtivoResponse]
)
def listar_ativos(
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    respostas = []

    for ativo in service.listar():
        try:
            cotacao = service.consultar_cotacao(
                ativo.codigo
            )

        except ValueError as erro:
            raise HTTPException(
                status_code=503,
                detail=str(erro)
            )

        respostas.append(
            montar_response(
                ativo,
                cotacao
            )
        )

    return respostas


@router.get(
    "/{codigo}",
    response_model=AtivoResponse
)
def consultar_ativo(
    codigo: str,
    db: Session = Depends(get_db)
):
    service = criar_service(db)

    try:
        ativo = service.consultar(
            codigo
        )

        cotacao = service.consultar_cotacao(
            codigo
        )

    except ValueError as erro:
        mensagem = str(erro)

        if mensagem == "Ativo não encontrado.":
            status_code = 404
        else:
            status_code = 503

        raise HTTPException(
            status_code=status_code,
            detail=mensagem
        )

    return montar_response(
        ativo,
        cotacao
    )