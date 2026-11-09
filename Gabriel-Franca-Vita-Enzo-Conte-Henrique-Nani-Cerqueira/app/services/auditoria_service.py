from sqlalchemy.orm import Session

from app.database.models import RegistroAuditoriaModel


class AuditoriaService:
    def __init__(self, db: Session):
        self._db = db

    def registrar(
        self,
        evento: str,
        resultado: str,
        ordem_id: int | None = None,
        investidor_id: int | None = None
    ) -> None:
        registro = RegistroAuditoriaModel(
            ordem_id=ordem_id,
            investidor_id=investidor_id,
            evento=evento,
            resultado=resultado
        )

        self._db.add(registro)
        self._db.commit()