from sqlalchemy.orm import Session

from app.database.models import ContaModel
from app.domain.conta import Conta


class ContaRepository:
    def __init__(self, db: Session):
        self._db = db

    def buscar_por_id(self, id_conta: int) -> Conta | None:
        model = (
            self._db.query(ContaModel)
            .filter(ContaModel.id == id_conta)
            .first()
        )

        if model is None:
            return None

        return Conta(
            id_conta=model.id,
            saldo_disponivel=model.saldo_disponivel,
            limite_risco=model.limite_risco,
            situacao=model.situacao
        )

    def atualizar(self, conta: Conta) -> None:
        model = (
            self._db.query(ContaModel)
            .filter(ContaModel.id == conta.id_conta)
            .first()
        )

        if model is None:
            raise ValueError("Conta não encontrada.")

        model.saldo_disponivel = conta.saldo_disponivel
        model.limite_risco = conta.limite_risco
        model.situacao = conta.situacao

        self._db.commit()