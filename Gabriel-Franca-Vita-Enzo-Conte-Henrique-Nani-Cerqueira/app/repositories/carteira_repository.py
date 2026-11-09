from sqlalchemy.orm import Session

from app.database.models import PosicaoCarteiraModel
from app.domain.carteira import Carteira, PosicaoCarteira


class CarteiraRepository:
    def __init__(self, db: Session):
        self._db = db

    def buscar_por_conta(self, id_conta: int) -> Carteira:
        models = (
            self._db.query(PosicaoCarteiraModel)
            .filter(PosicaoCarteiraModel.conta_id == id_conta)
            .all()
        )

        carteira = Carteira(id_carteira=id_conta)

        for model in models:
            carteira._posicoes[model.codigo_ativo] = PosicaoCarteira(
                codigo_ativo=model.codigo_ativo,
                quantidade=model.quantidade,
                quantidade_disponivel=model.quantidade_disponivel
            )

        return carteira

    def atualizar(self, carteira: Carteira) -> None:
        for codigo_ativo, posicao in carteira._posicoes.items():
            model = (
                self._db.query(PosicaoCarteiraModel)
                .filter(
                    PosicaoCarteiraModel.conta_id == carteira.id_carteira,
                    PosicaoCarteiraModel.codigo_ativo == codigo_ativo
                )
                .first()
            )

            if model is None:
                model = PosicaoCarteiraModel(
                    conta_id=carteira.id_carteira,
                    codigo_ativo=codigo_ativo,
                    quantidade=posicao.quantidade,
                    quantidade_disponivel=posicao.quantidade_disponivel
                )

                self._db.add(model)

            else:
                model.quantidade = posicao.quantidade
                model.quantidade_disponivel = posicao.quantidade_disponivel

        self._db.commit()