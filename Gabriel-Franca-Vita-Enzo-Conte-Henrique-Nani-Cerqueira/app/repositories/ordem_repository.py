from sqlalchemy.orm import Session

from app.database.models import OrdemModel
from app.domain.enums import EstadoOrdem, TipoOrdem
from app.domain.ordem import Ordem


class OrdemRepository:
    def __init__(self, db: Session):
        self._db = db

    def salvar(self, ordem: Ordem, chave_idempotencia: str) -> Ordem:
        model = OrdemModel(
            conta_id=ordem.id_conta,
            codigo_ativo=ordem.codigo_ativo,
            tipo=ordem.tipo.value,
            quantidade=ordem.quantidade,
            quantidade_executada=ordem.quantidade_executada,
            preco=ordem.preco,
            preco_medio_execucao=ordem.preco_medio_execucao,
            estado=ordem.estado.value,
            chave_idempotencia=chave_idempotencia,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        ordem._id_ordem = model.id
        return ordem

    def atualizar(self, ordem: Ordem) -> Ordem:
        model = self._db.query(OrdemModel).filter(OrdemModel.id == ordem.id_ordem).first()
        if model is None:
            raise ValueError("Ordem não encontrada.")
        model.estado = ordem.estado.value
        model.quantidade = ordem.quantidade
        model.quantidade_executada = ordem.quantidade_executada
        model.preco = ordem.preco
        model.preco_medio_execucao = ordem.preco_medio_execucao
        self._db.commit()
        self._db.refresh(model)
        return ordem

    def _converter_model(self, model: OrdemModel) -> Ordem:
        ordem = Ordem(
            id_ordem=model.id,
            id_conta=model.conta_id,
            codigo_ativo=model.codigo_ativo,
            tipo=TipoOrdem(model.tipo),
            quantidade=model.quantidade,
            preco=model.preco,
            quantidade_executada=getattr(model, "quantidade_executada", 0) or 0,
            preco_medio_execucao=getattr(model, "preco_medio_execucao", None),
        )
        ordem._estado = EstadoOrdem(model.estado)
        return ordem

    def buscar_por_id(self, id_ordem: int) -> Ordem | None:
        model = self._db.query(OrdemModel).filter(OrdemModel.id == id_ordem).first()
        return None if model is None else self._converter_model(model)

    def listar(self) -> list[Ordem]:
        return [self._converter_model(m) for m in self._db.query(OrdemModel).order_by(OrdemModel.criada_em.desc()).all()]

    def listar_por_conta(self, conta_id: int) -> list[Ordem]:
        models = self._db.query(OrdemModel).filter(OrdemModel.conta_id == conta_id).order_by(OrdemModel.criada_em.desc()).all()
        return [self._converter_model(m) for m in models]

    def existe_chave_duplicidade(self, chave_idempotencia: str) -> bool:
        return self._db.query(OrdemModel).filter(OrdemModel.chave_idempotencia == chave_idempotencia).first() is not None
