from app.domain.enums import EstadoOrdem, TipoOrdem


class Ordem:
    def __init__(
        self,
        id_ordem: int | None,
        id_conta: int,
        codigo_ativo: str,
        tipo: TipoOrdem,
        quantidade: int,
        preco: float
    ):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")

        if preco <= 0:
            raise ValueError("O preço deve ser maior que zero.")

        self._id_ordem = id_ordem
        self._id_conta = id_conta
        self._codigo_ativo = codigo_ativo
        self._tipo = tipo
        self._quantidade = quantidade
        self._preco = preco
        self._estado = EstadoOrdem.CRIADA

    @property
    def id_ordem(self) -> int | None:
        return self._id_ordem

    @property
    def id_conta(self) -> int:
        return self._id_conta

    @property
    def codigo_ativo(self) -> str:
        return self._codigo_ativo

    @property
    def tipo(self) -> TipoOrdem:
        return self._tipo

    @property
    def quantidade(self) -> int:
        return self._quantidade

    @property
    def preco(self) -> float:
        return self._preco

    @property
    def estado(self) -> EstadoOrdem:
        return self._estado

    def validar(self) -> None:
        if self._estado != EstadoOrdem.CRIADA:
            raise ValueError(
                "Apenas ordens criadas podem ser validadas."
            )

        self._estado = EstadoOrdem.VALIDADA

    def enviar(self) -> None:
        if self._estado != EstadoOrdem.VALIDADA:
            raise ValueError(
                "Apenas ordens validadas podem ser enviadas."
            )

        self._estado = EstadoOrdem.ENVIADA

    def executar_parcialmente(self) -> None:
        if self._estado not in {
            EstadoOrdem.ENVIADA,
            EstadoOrdem.PARCIALMENTE_EXECUTADA
        }:
            raise ValueError(
                "A ordem não pode ser parcialmente executada neste estado."
            )

        self._estado = EstadoOrdem.PARCIALMENTE_EXECUTADA

    def executar(self) -> None:
        if self._estado not in {
            EstadoOrdem.ENVIADA,
            EstadoOrdem.PARCIALMENTE_EXECUTADA
        }:
            raise ValueError(
                "A ordem não pode ser executada neste estado."
            )

        self._estado = EstadoOrdem.EXECUTADA

    def rejeitar(self) -> None:
        if self._estado not in {
            EstadoOrdem.CRIADA,
            EstadoOrdem.ENVIADA
        }:
            raise ValueError(
                "A ordem não pode ser rejeitada neste estado."
            )

        self._estado = EstadoOrdem.REJEITADA

    def cancelar(self) -> None:
        if self._estado not in {
            EstadoOrdem.VALIDADA,
            EstadoOrdem.ENVIADA,
            EstadoOrdem.PARCIALMENTE_EXECUTADA
        }:
            raise ValueError(
                "A ordem não pode ser cancelada neste estado."
            )

        self._estado = EstadoOrdem.CANCELADA

    def atualizar(
        self,
        quantidade: int | None = None,
        preco: float | None = None
    ) -> None:
        if self._estado not in {
            EstadoOrdem.CRIADA,
            EstadoOrdem.VALIDADA
        }:
            raise ValueError(
                "A ordem não pode ser atualizada neste estado."
            )

        if quantidade is not None:
            if quantidade <= 0:
                raise ValueError(
                    "A quantidade deve ser maior que zero."
                )

            self._quantidade = quantidade

        if preco is not None:
            if preco <= 0:
                raise ValueError(
                    "O preço deve ser maior que zero."
                )

            self._preco = preco