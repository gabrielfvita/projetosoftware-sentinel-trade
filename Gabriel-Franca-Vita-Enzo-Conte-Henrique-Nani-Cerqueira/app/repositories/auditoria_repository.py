from sqlalchemy.orm import Session

from app.database.models import RegistroAuditoriaModel


class AuditoriaRepository:
    def __init__(
        self,
        db: Session
    ):
        self._db = db

    def listar_por_ordem(
        self,
        ordem_id: int
    ) -> list[RegistroAuditoriaModel]:
        return (
            self._db.query(
                RegistroAuditoriaModel
            )
            .filter(
                RegistroAuditoriaModel.ordem_id
                == ordem_id
            )
            .order_by(
                RegistroAuditoriaModel.data_hora
            )
            .all()
        )

    def listar_por_investidor(
        self,
        investidor_id: int
    ) -> list[RegistroAuditoriaModel]:
        return (
            self._db.query(
                RegistroAuditoriaModel
            )
            .filter(
                RegistroAuditoriaModel.investidor_id
                == investidor_id
            )
            .order_by(
                RegistroAuditoriaModel.data_hora.desc()
            )
            .all()
        )