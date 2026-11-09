from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.repositories.carteira_repository import CarteiraRepository
from app.repositories.conta_repository import ContaRepository
from app.schemas.carteira import CarteiraResponse, PosicaoResponse
from app.security.session import exigir_conta_do_investidor, investidor_atual
from app.services.carteira_service import CarteiraService

router = APIRouter(prefix="/carteiras", tags=["Carteiras"])


def _response(db: Session, conta_id: int):
    service = CarteiraService(ContaRepository(db), CarteiraRepository(db))
    try:
        conta, carteira = service.consultar(conta_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))
    return CarteiraResponse(
        conta_id=conta.id_conta, saldo_disponivel=conta.saldo_disponivel,
        limite_risco=conta.limite_risco, situacao=conta.situacao,
        posicoes=[PosicaoResponse(codigo_ativo=p.codigo_ativo, quantidade=p.quantidade, quantidade_disponivel=p.quantidade_disponivel) for p in carteira._posicoes.values()]
    )


@router.get("/minha", response_model=CarteiraResponse)
def minha_carteira(db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    conta = ContaRepository(db).buscar_primeira_por_investidor(investidor.id)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")
    return _response(db, conta.id)


@router.get("/{conta_id}", response_model=CarteiraResponse)
def consultar_carteira(conta_id: int, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    exigir_conta_do_investidor(db, conta_id, investidor.id)
    return _response(db, conta_id)
