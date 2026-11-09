from app.domain.enums import TipoAtivo


class Ativo:
    def __init__(
        self,
        codigo: str,
        nome: str,
        tipo: TipoAtivo,
        cotacao: float
    ):
        self._codigo = codigo
        self._nome = nome
        self._tipo = tipo
        self._cotacao = cotacao

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def tipo(self) -> TipoAtivo:
        return self._tipo

    @property
    def cotacao(self) -> float:
        return self._cotacao

    def atualizar_cotacao(self, nova_cotacao: float) -> None:
        if nova_cotacao <= 0:
            raise ValueError("A cotação deve ser maior que zero.")

        self._cotacao = nova_cotacao