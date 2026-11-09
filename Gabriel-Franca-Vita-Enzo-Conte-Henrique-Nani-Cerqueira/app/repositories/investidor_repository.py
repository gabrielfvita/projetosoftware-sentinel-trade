from sqlalchemy.orm import Session

from app.database.models import InvestidorModel


class InvestidorRepository:
    def __init__(self, db: Session):
        self._db = db

    def criar(
        self,
        nome: str,
        email: str,
        senha_hash: str
    ) -> InvestidorModel:
        model = InvestidorModel(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            mfa_habilitado=True,
            status="ativo"
        )

        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)

        return model

    def buscar_por_email(
        self,
        email: str
    ) -> InvestidorModel | None:
        return (
            self._db.query(InvestidorModel)
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
            self._db.query(InvestidorModel)
            .filter(
                InvestidorModel.id == investidor_id
            )
            .first()
        )

    def listar(self) -> list[InvestidorModel]:
        return (
            self._db.query(InvestidorModel)
            .all()
        )

    def atualizar(
        self,
        investidor: InvestidorModel
    ) -> InvestidorModel:
        self._db.commit()
        self._db.refresh(investidor)

        return investidor