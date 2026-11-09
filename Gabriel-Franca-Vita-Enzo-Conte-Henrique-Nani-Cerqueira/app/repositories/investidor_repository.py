from sqlalchemy.orm import Session

from app.database.models import InvestidorModel


class InvestidorRepository:
    def __init__(
        self,
        db: Session
    ):
        self._db = db

    def buscar_por_email(
        self,
        email: str
    ) -> InvestidorModel | None:
        return (
            self._db
            .query(InvestidorModel)
            .filter(
                InvestidorModel.email == email
            )
            .first()
        )

    def buscar_por_id(
        self,
        investidor_id: int
    ) -> InvestidorModel | None:
        return (
            self._db
            .query(InvestidorModel)
            .filter(
                InvestidorModel.id == investidor_id
            )
            .first()
        )