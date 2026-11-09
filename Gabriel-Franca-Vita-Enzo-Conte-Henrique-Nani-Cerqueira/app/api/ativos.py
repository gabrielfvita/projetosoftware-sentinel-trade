from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.integrations.cotacao_simulada import CotacaoSimulada
from app.repositories.ativo_repository import AtivoRepository
from app.schemas.ativo import AtivoResponse
from app.security.session import investidor_atual
from app.services.ativo_service import AtivoService

router = APIRouter(prefix="/ativos", tags=["Ativos"])


def criar_service(db): return AtivoService(AtivoRepository(db), CotacaoSimulada())
def montar_response(a, c): return AtivoResponse(codigo=a.codigo, nome=a.nome, tipo=a.tipo.value, cotacao=c)


@router.get("", response_model=list[AtivoResponse])
def listar_ativos(db: Session = Depends(get_db), _=Depends(investidor_atual)):
    service = criar_service(db)
    respostas=[]
    for ativo in service.listar():
        try: cotacao=service.consultar_cotacao(ativo.codigo)
        except ValueError as erro: raise HTTPException(status_code=503, detail=str(erro))
        respostas.append(montar_response(ativo,cotacao))
    return respostas


@router.get("/{codigo}", response_model=AtivoResponse)
def consultar_ativo(codigo: str, db: Session = Depends(get_db), _=Depends(investidor_atual)):
    service=criar_service(db)
    try:
        ativo=service.consultar(codigo); cotacao=service.consultar_cotacao(codigo)
    except ValueError as erro:
        raise HTTPException(status_code=404 if str(erro)=="Ativo não encontrado." else 503, detail=str(erro))
    return montar_response(ativo,cotacao)
