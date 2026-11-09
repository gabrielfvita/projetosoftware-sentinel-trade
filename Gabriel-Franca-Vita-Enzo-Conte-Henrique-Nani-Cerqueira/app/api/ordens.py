from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.domain.ordem import Ordem
from app.repositories.ativo_repository import AtivoRepository
from app.integrations.cotacao_simulada import CotacaoSimulada
from app.repositories.carteira_repository import CarteiraRepository
from app.repositories.conta_repository import ContaRepository
from app.repositories.ordem_repository import OrdemRepository
from app.schemas.ordem import OrdemCreate, OrdemResponse, OrdemUpdate
from app.security.session import exigir_conta_do_investidor, investidor_atual
from app.services.auditoria_service import AuditoriaService
from app.services.ordem_service import OrdemService
from app.services.validacao_service import ValidacaoService

router = APIRouter(prefix="/ordens", tags=["Ordens"])


def criar_service(db: Session) -> OrdemService:
    return OrdemService(OrdemRepository(db), ValidacaoService(), AuditoriaService(db), ContaRepository(db), CarteiraRepository(db), AtivoRepository(db), CotacaoSimulada())


def montar_response(ordem: Ordem) -> OrdemResponse:
    return OrdemResponse(
        id_ordem=ordem.id_ordem, conta_id=ordem.id_conta, codigo_ativo=ordem.codigo_ativo,
        tipo=ordem.tipo.value, quantidade=ordem.quantidade,
        quantidade_executada=ordem.quantidade_executada,
        quantidade_remanescente=ordem.quantidade_remanescente,
        preco=ordem.preco, preco_limite=ordem.preco_limite,
        preco_medio_execucao=ordem.preco_medio_execucao, estado=ordem.estado.value,
    )


def _ordem_do_investidor(db: Session, id_ordem: int, investidor_id: int) -> Ordem:
    ordem = OrdemRepository(db).buscar_por_id(id_ordem)
    if ordem is None:
        raise HTTPException(status_code=404, detail="Ordem não encontrada.")
    exigir_conta_do_investidor(db, ordem.id_conta, investidor_id)
    return ordem


@router.post("", response_model=OrdemResponse, status_code=status.HTTP_201_CREATED)
def criar_ordem(dados: OrdemCreate, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    exigir_conta_do_investidor(db, dados.conta_id, investidor.id)
    conta_repo, carteira_repo = ContaRepository(db), CarteiraRepository(db)
    conta = conta_repo.buscar_por_id(dados.conta_id)
    ativo = AtivoRepository(db).buscar_por_codigo(dados.codigo_ativo)
    if ativo is None:
        raise HTTPException(status_code=404, detail="Ativo não encontrado.")
    ordem = Ordem(None, dados.conta_id, dados.codigo_ativo, dados.tipo, dados.quantidade, dados.preco)
    try:
        ordem = criar_service(db).criar_ordem(ordem, conta, carteira_repo.buscar_por_conta(dados.conta_id), dados.chave_idempotencia)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    return montar_response(ordem)


@router.get("/{id_ordem}", response_model=OrdemResponse)
def consultar_ordem(id_ordem: int, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    return montar_response(_ordem_do_investidor(db, id_ordem, investidor.id))


@router.patch("/{id_ordem}", response_model=OrdemResponse)
def atualizar_ordem(id_ordem: int, dados: OrdemUpdate, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    ordem_existente = _ordem_do_investidor(db, id_ordem, investidor.id)
    conta_repo, carteira_repo = ContaRepository(db), CarteiraRepository(db)
    try:
        ordem = criar_service(db).atualizar_ordem(id_ordem, conta_repo.buscar_por_id(ordem_existente.id_conta), carteira_repo.buscar_por_conta(ordem_existente.id_conta), dados.quantidade, dados.preco)
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
    return montar_response(ordem)


@router.patch("/{id_ordem}/cancelar", response_model=OrdemResponse)
def cancelar_ordem(id_ordem: int, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    _ordem_do_investidor(db, id_ordem, investidor.id)
    try:
        return montar_response(criar_service(db).cancelar_ordem(id_ordem))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.post("/{id_ordem}/processar", response_model=OrdemResponse, include_in_schema=False)
def processar_ordem(id_ordem: int, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    _ordem_do_investidor(db, id_ordem, investidor.id)
    try:
        return montar_response(criar_service(db).processar_ordem(id_ordem))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))


@router.post("/{id_ordem}/reconciliar", response_model=OrdemResponse, include_in_schema=False)
def reconciliar_ordem(id_ordem: int, db: Session = Depends(get_db), investidor=Depends(investidor_atual)):
    _ordem_do_investidor(db, id_ordem, investidor.id)
    try:
        return montar_response(criar_service(db).reconciliar_ordem(id_ordem))
    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro))
