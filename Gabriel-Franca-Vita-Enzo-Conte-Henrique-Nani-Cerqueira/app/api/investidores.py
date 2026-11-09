from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.investidor_repository import InvestidorRepository
from app.schemas.investidor import InvestidorResponse, InvestidorUpdate
from app.security.session import investidor_atual
from app.services.auditoria_service import AuditoriaService
from app.services.investidor_service import InvestidorService

router = APIRouter(prefix="/investidores", tags=["Investidores"])


def criar_service(db): return InvestidorService(InvestidorRepository(db), AuditoriaService(db))
def montar_response(i): return InvestidorResponse(id=i.id,nome=i.nome,email=i.email,status=i.status,mfa_habilitado=i.mfa_habilitado)


@router.get("/me", response_model=InvestidorResponse)
def consultar_me(investidor=Depends(investidor_atual)):
    return montar_response(investidor)


@router.patch("/me", response_model=InvestidorResponse)
def atualizar_me(dados: InvestidorUpdate, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    try:
        atualizado=criar_service(db).atualizar(investidor.id,dados.nome,str(dados.email) if dados.email is not None else None)
    except ValueError as erro:
        raise HTTPException(status_code=400,detail=str(erro))
    return montar_response(atualizado)


@router.get("", response_model=list[InvestidorResponse], include_in_schema=False)
def listar_investidores(investidor=Depends(investidor_atual)):
    return [montar_response(investidor)]


@router.get("/{investidor_id}", response_model=InvestidorResponse, include_in_schema=False)
def consultar_investidor(investidor_id:int,investidor=Depends(investidor_atual)):
    if investidor_id != investidor.id:
        raise HTTPException(status_code=403,detail="Acesso não autorizado.")
    return montar_response(investidor)
