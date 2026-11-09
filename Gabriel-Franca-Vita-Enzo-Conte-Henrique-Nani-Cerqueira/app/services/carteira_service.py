from app.repositories.carteira_repository import CarteiraRepository
from app.repositories.conta_repository import ContaRepository


class CarteiraService:
    def __init__(
        self,
        conta_repository: ContaRepository,
        carteira_repository: CarteiraRepository
    ):
        self._conta_repository = conta_repository
        self._carteira_repository = carteira_repository

    def consultar(self, conta_id: int):
        conta = self._conta_repository.buscar_por_id(conta_id)

        if conta is None:
            raise ValueError("Conta não encontrada.")

        carteira = self._carteira_repository.buscar_por_conta(
            conta_id
        )

        return conta, carteira