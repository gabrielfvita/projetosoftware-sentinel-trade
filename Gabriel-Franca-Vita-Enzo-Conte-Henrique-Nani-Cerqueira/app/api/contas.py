from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.conta_repository import ContaRepository
from app.repositories.investidor_repository import InvestidorRepository
from app.schemas.conta import ContaCreate, ContaResponse, ContaUpdate
from app.security.session import exigir_conta_do_investidor, investidor_atual
from app.services.auditoria_service import AuditoriaService
from app.services.conta_service import ContaService

router = APIRouter(prefix="/contas", tags=["Contas"])


def criar_service(db: Session):
    return ContaService(ContaRepository(db), InvestidorRepository(db), AuditoriaService(db))


def montar_response(conta):
    return ContaResponse(id=conta.id, investidor_id=conta.investidor_id, saldo_disponivel=conta.saldo_disponivel, limite_risco=conta.limite_risco, situacao=conta.situacao)


@router.get("/minha-conta", response_model=ContaResponse)
def minha_conta(db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    conta = ContaRepository(db).buscar_primeira_por_investidor(investidor.id)
    if conta is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada.")
    return montar_response(conta)


@router.post("", response_model=ContaResponse, status_code=status.HTTP_201_CREATED, include_in_schema=False)
def criar_conta(dados: ContaCreate, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    if dados.investidor_id != investidor.id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    try:
        return montar_response(criar_service(db).criar(dados.investidor_id, dados.saldo_inicial, dados.limite_risco))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.get("/{conta_id}", response_model=ContaResponse)
def consultar_conta(conta_id: int, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    exigir_conta_do_investidor(db, conta_id, investidor.id)
    try:
        return montar_response(criar_service(db).consultar(conta_id))
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))


@router.get("/investidor/{investidor_id}", response_model=list[ContaResponse])
def listar_contas_investidor(investidor_id: int, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    if investidor_id != investidor.id:
        raise HTTPException(status_code=403, detail="Acesso não autorizado.")
    return [montar_response(c) for c in criar_service(db).listar_por_investidor(investidor_id)]


@router.patch("/{conta_id}", response_model=ContaResponse)
def atualizar_conta(conta_id: int, dados: ContaUpdate, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    exigir_conta_do_investidor(db, conta_id, investidor.id)
    if dados.limite_risco is None:
        raise HTTPException(status_code=400, detail="Nenhum campo válido foi informado.")
    try:
        return montar_response(criar_service(db).atualizar_limite(conta_id, dados.limite_risco))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.patch("/{conta_id}/bloquear", response_model=ContaResponse, include_in_schema=False)
def bloquear_conta(conta_id: int, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    exigir_conta_do_investidor(db, conta_id, investidor.id)
    return montar_response(criar_service(db).bloquear(conta_id))


@router.patch("/{conta_id}/ativar", response_model=ContaResponse, include_in_schema=False)
def ativar_conta(conta_id: int, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    exigir_conta_do_investidor(db, conta_id, investidor.id)
    return montar_response(criar_service(db).ativar(conta_id))
