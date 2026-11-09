from sqlalchemy.orm import Session

from app.database.models import AtivoModel
from app.domain.ativo import Ativo
from app.domain.enums import TipoAtivo


class AtivoRepository:
    def __init__(self, db: Session):
        self._db = db

    def buscar_por_codigo(self, codigo: str) -> Ativo | None:
        codigo = codigo.strip().upper()

        model = (
            self._db.query(AtivoModel)
            .filter(AtivoModel.codigo == codigo)
            .first()
        )

        if model is None:
            return None

        return Ativo(
            codigo=model.codigo,
            nome=model.nome,
            tipo=TipoAtivo(model.tipo),
            cotacao=model.cotacao
        )

    def listar(self) -> list[Ativo]:
        models = self._db.query(AtivoModel).all()

        return [
            Ativo(
                codigo=model.codigo,
                nome=model.nome,
                tipo=TipoAtivo(model.tipo),
                cotacao=model.cotacao
            )
            for model in models
        ]