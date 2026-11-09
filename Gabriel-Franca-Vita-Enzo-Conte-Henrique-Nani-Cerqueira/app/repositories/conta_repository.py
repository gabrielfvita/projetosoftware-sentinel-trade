from sqlalchemy.orm import Session

from app.database.models import ContaModel
from app.domain.conta import Conta


class ContaRepository:
    def __init__(self, db: Session):
        self._db = db

    def criar(
        self,
        investidor_id: int,
        saldo_disponivel: float,
        limite_risco: float
    ) -> ContaModel:
        model = ContaModel(
            investidor_id=investidor_id,
            saldo_disponivel=saldo_disponivel,
            limite_risco=limite_risco,
            situacao="ativa"
        )

        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)

        return model

    def buscar_model_por_id(
        self,
        id_conta: int
    ) -> ContaModel | None:
        return (
            self._db.query(ContaModel)
            .filter(ContaModel.id == id_conta)
            .first()
        )

    def buscar_por_id(
        self,
        id_conta: int
    ) -> Conta | None:
        model = self.buscar_model_por_id(
            id_conta
        )

        if model is None:
            return None

        return Conta(
            id_conta=model.id,
            saldo_disponivel=model.saldo_disponivel,
            limite_risco=model.limite_risco,
            situacao=model.situacao
        )

    def listar_por_investidor(
        self,
        investidor_id: int
    ) -> list[ContaModel]:
        return (
            self._db.query(ContaModel)
            .filter(
                ContaModel.investidor_id == investidor_id
            )
            .all()
        )


    def buscar_primeira_por_investidor(self, investidor_id: int) -> ContaModel | None:
        return (
            self._db.query(ContaModel)
            .filter(ContaModel.investidor_id == investidor_id)
            .order_by(ContaModel.id)
            .first()
        )

    def buscar_investidor_id(self, conta_id: int) -> int | None:
        model = self.buscar_model_por_id(conta_id)
        return None if model is None else model.investidor_id

    def atualizar(
        self,
        conta: Conta
    ) -> None:
        model = self.buscar_model_por_id(
            conta.id_conta
        )

        if model is None:
            raise ValueError(
                "Conta não encontrada."
            )

        model.saldo_disponivel = (
            conta.saldo_disponivel
        )

        model.limite_risco = (
            conta.limite_risco
        )

        model.situacao = (
            conta.situacao
        )

        self._db.commit()
        self._db.refresh(model)

    def atualizar_model(
        self,
        model: ContaModel
    ) -> ContaModel:
        self._db.commit()
        self._db.refresh(model)

        return model