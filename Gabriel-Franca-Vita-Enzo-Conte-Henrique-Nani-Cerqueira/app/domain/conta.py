class Conta:
    def __init__(
        self,
        id_conta: int,
        saldo_disponivel: float,
        limite_risco: float,
        situacao: str = "ativa"
    ):
        if saldo_disponivel < 0:
            raise ValueError("O saldo disponível não pode ser negativo.")

        if limite_risco <= 0:
            raise ValueError("O limite de risco deve ser maior que zero.")

        self._id_conta = id_conta
        self._saldo_disponivel = saldo_disponivel
        self._limite_risco = limite_risco
        self._situacao = situacao

    @property
    def id_conta(self) -> int:
        return self._id_conta

    @property
    def saldo_disponivel(self) -> float:
        return self._saldo_disponivel

    @property
    def limite_risco(self) -> float:
        return self._limite_risco

    @property
    def situacao(self) -> str:
        return self._situacao

    def debitar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor do débito deve ser maior que zero.")

        if valor > self._saldo_disponivel:
            raise ValueError("Saldo insuficiente.")

        self._saldo_disponivel -= valor

    def creditar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("O valor do crédito deve ser maior que zero.")

        self._saldo_disponivel += valor

    def bloquear(self) -> None:
        self._situacao = "bloqueada"

    def ativar(self) -> None:
        self._situacao = "ativa"