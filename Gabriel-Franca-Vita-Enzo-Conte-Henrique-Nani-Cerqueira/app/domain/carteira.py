class PosicaoCarteira:
    def __init__(
        self,
        codigo_ativo: str,
        quantidade: int,
        quantidade_disponivel: int
    ):
        if quantidade < 0:
            raise ValueError("A quantidade não pode ser negativa.")

        if quantidade_disponivel < 0:
            raise ValueError("A quantidade disponível não pode ser negativa.")

        if quantidade_disponivel > quantidade:
            raise ValueError(
                "A quantidade disponível não pode ser maior que a quantidade total."
            )

        self._codigo_ativo = codigo_ativo
        self._quantidade = quantidade
        self._quantidade_disponivel = quantidade_disponivel

    @property
    def codigo_ativo(self) -> str:
        return self._codigo_ativo

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @property
    def quantidade_disponivel(self) -> int:
        return self._quantidade_disponivel

    def adicionar(self, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        self._quantidade += quantidade
        self._quantidade_disponivel += quantidade

    def remover(self, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        if quantidade > self._quantidade_disponivel:
            raise ValueError("Posição disponível insuficiente.")

        self._quantidade -= quantidade
        self._quantidade_disponivel -= quantidade


class Carteira:
    def __init__(self, id_carteira: int):
        self._id_carteira = id_carteira
        self._posicoes: dict[str, PosicaoCarteira] = {}

    @property
    def id_carteira(self) -> int:
        return self._id_carteira

    def consultar_posicao(
        self,
        codigo_ativo: str
    ) -> PosicaoCarteira | None:
        return self._posicoes.get(codigo_ativo)

    def adicionar_ativo(
        self,
        codigo_ativo: str,
        quantidade: int
    ) -> None:
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        posicao = self._posicoes.get(codigo_ativo)

        if posicao:
            posicao.adicionar(quantidade)
        else:
            self._posicoes[codigo_ativo] = PosicaoCarteira(
                codigo_ativo=codigo_ativo,
                quantidade=quantidade,
                quantidade_disponivel=quantidade
            )

    def remover_ativo(
        self,
        codigo_ativo: str,
        quantidade: int
    ) -> None:
        posicao = self._posicoes.get(codigo_ativo)

        if posicao is None:
            raise ValueError("Ativo não encontrado na carteira.")

        posicao.remover(quantidade)

        if posicao.quantidade == 0:
            del self._posicoes[codigo_ativo]