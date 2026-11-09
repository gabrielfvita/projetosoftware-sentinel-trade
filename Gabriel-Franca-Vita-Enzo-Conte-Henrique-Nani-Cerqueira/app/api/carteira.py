from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.repositories.carteira_repository import (
    CarteiraRepository
)
from app.repositories.conta_repository import (
    ContaRepository
)

from app.schemas.carteira import (
    CarteiraResponse,
    PosicaoResponse
)

from app.services.carteira_service import (
    CarteiraService
)


router = APIRouter(
    prefix="/carteiras",
    tags=["Carteiras"]
)


@router.get(
    "/{conta_id}",
    response_model=CarteiraResponse
)
def consultar_carteira(
    conta_id: int,
    db: Session = Depends(get_db)
):
    service = CarteiraService(
        conta_repository=ContaRepository(db),
        carteira_repository=CarteiraRepository(db)
    )

    try:
        conta, carteira = service.consultar(
            conta_id
        )

    except ValueError as erro:
        raise HTTPException(
            status_code=404,
            detail=str(erro)
        )

    posicoes = []

    for posicao in carteira._posicoes.values():
        posicoes.append(
            PosicaoResponse(
                codigo_ativo=posicao.codigo_ativo,
                quantidade=posicao.quantidade,
                quantidade_disponivel=(
                    posicao.quantidade_disponivel
                )
            )
        )

    return CarteiraResponse(
        conta_id=conta.id_conta,
        saldo_disponivel=conta.saldo_disponivel,
        limite_risco=conta.limite_risco,
        situacao=conta.situacao,
        posicoes=posicoes
    )