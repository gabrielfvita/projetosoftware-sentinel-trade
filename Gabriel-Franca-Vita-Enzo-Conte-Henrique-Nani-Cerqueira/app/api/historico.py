from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.repositories.auditoria_repository import AuditoriaRepository
from app.repositories.conta_repository import ContaRepository
from app.repositories.ordem_repository import OrdemRepository
from app.schemas.historico import AuditoriaResponse, HistoricoOrdemResponse
from app.security.session import exigir_conta_do_investidor, investidor_atual
from app.services.historico_service import HistoricoService

router=APIRouter(prefix="/historico",tags=["Histórico"])

def service(db): return HistoricoService(OrdemRepository(db),ContaRepository(db),AuditoriaRepository(db))
def ordem_resp(o): return HistoricoOrdemResponse(id_ordem=o.id_ordem,conta_id=o.id_conta,codigo_ativo=o.codigo_ativo,tipo=o.tipo.value,quantidade=o.quantidade,quantidade_executada=o.quantidade_executada,quantidade_remanescente=o.quantidade_remanescente,preco=o.preco,preco_limite=o.preco_limite,preco_medio_execucao=o.preco_medio_execucao,estado=o.estado.value)

@router.get("/minhas-ordens",response_model=list[HistoricoOrdemResponse])
def minhas_ordens(db:Session=Depends(get_db),investidor=Depends(investidor_atual)):
    conta=ContaRepository(db).buscar_primeira_por_investidor(investidor.id)
    if conta is None: raise HTTPException(status_code=404,detail="Conta não encontrada.")
    return [ordem_resp(o) for o in service(db).listar_ordens_conta(conta.id)]

@router.get("/contas/{conta_id}/ordens",response_model=list[HistoricoOrdemResponse])
def historico(conta_id:int,db:Session=Depends(get_db),investidor=Depends(investidor_atual)):
    exigir_conta_do_investidor(db,conta_id,investidor.id)
    return [ordem_resp(o) for o in service(db).listar_ordens_conta(conta_id)]

@router.get("/ordens/{ordem_id}/auditoria",response_model=list[AuditoriaResponse])
def auditoria(ordem_id:int,db:Session=Depends(get_db),investidor=Depends(investidor_atual)):
    ordem=OrdemRepository(db).buscar_por_id(ordem_id)
    if ordem is None: raise HTTPException(status_code=404,detail="Ordem não encontrada.")
    exigir_conta_do_investidor(db,ordem.id_conta,investidor.id)
    regs=service(db).listar_auditoria_ordem(ordem_id)
    return [AuditoriaResponse(id=r.id,ordem_id=r.ordem_id,investidor_id=r.investidor_id,evento=r.evento,resultado=r.resultado,data_hora=r.data_hora) for r in regs]
