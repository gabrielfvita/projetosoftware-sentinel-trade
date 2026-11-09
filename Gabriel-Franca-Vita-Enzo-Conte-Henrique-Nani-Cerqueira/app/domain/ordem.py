from app.domain.enums import EstadoOrdem, TipoOrdem


class Ordem:
    def __init__(
        self,
        id_ordem: int | None,
        id_conta: int,
        codigo_ativo: str,
        tipo: TipoOrdem,
        quantidade: int,
        preco: float,
        quantidade_executada: int = 0,
        preco_medio_execucao: float | None = None,
    ):
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        if preco <= 0:
            raise ValueError("O preco limite deve ser maior que zero.")
        if quantidade_executada < 0 or quantidade_executada > quantidade:
            raise ValueError("Quantidade executada invalida.")
        if preco_medio_execucao is not None and preco_medio_execucao <= 0:
            raise ValueError("Preco medio de execucao invalido.")

        self._id_ordem = id_ordem
        self._id_conta = id_conta
        self._codigo_ativo = codigo_ativo
        self._tipo = tipo
        self._quantidade = quantidade
        self._preco = preco
        self._quantidade_executada = quantidade_executada
        self._preco_medio_execucao = preco_medio_execucao
        self._estado = EstadoOrdem.CRIADA

    @property
    def id_ordem(self): return self._id_ordem
    @property
    def id_conta(self): return self._id_conta
    @property
    def codigo_ativo(self): return self._codigo_ativo
    @property
    def tipo(self): return self._tipo
    @property
    def quantidade(self): return self._quantidade
    @property
    def preco(self): return self._preco
    @property
    def preco_limite(self): return self._preco
    @property
    def preco_medio_execucao(self): return self._preco_medio_execucao
    @property
    def estado(self): return self._estado
    @property
    def quantidade_executada(self): return self._quantidade_executada
    @property
    def quantidade_remanescente(self): return self._quantidade - self._quantidade_executada

    def validar(self) -> None:
        if self._estado != EstadoOrdem.CRIADA:
            raise ValueError("Apenas ordens criadas podem ser validadas.")
        self._estado = EstadoOrdem.VALIDADA

    def enviar(self) -> None:
        if self._estado != EstadoOrdem.VALIDADA:
            raise ValueError("Apenas ordens validadas podem ser enviadas.")
        self._estado = EstadoOrdem.ENVIADA

    def registrar_execucao(self, quantidade: int, preco_execucao: float | None = None) -> None:
        if self._estado not in {EstadoOrdem.ENVIADA, EstadoOrdem.PARCIALMENTE_EXECUTADA}:
            raise ValueError("A ordem nao pode ser executada neste estado.")
        if quantidade <= 0 or quantidade > self.quantidade_remanescente:
            raise ValueError("Quantidade de execucao invalida.")

        preco = self._preco if preco_execucao is None else preco_execucao
        if preco <= 0:
            raise ValueError("Preco de execucao invalido.")

        valor_anterior = (self._preco_medio_execucao or 0) * self._quantidade_executada
        nova_quantidade = self._quantidade_executada + quantidade
        self._preco_medio_execucao = (valor_anterior + preco * quantidade) / nova_quantidade
        self._quantidade_executada = nova_quantidade

        if self._quantidade_executada == self._quantidade:
            self._estado = EstadoOrdem.EXECUTADA
        else:
            self._estado = EstadoOrdem.PARCIALMENTE_EXECUTADA

    def executar_parcialmente(self, quantidade: int | None = None, preco_execucao: float | None = None) -> None:
        restante = self.quantidade_remanescente
        if restante <= 1:
            raise ValueError("Nao ha quantidade suficiente para execucao parcial.")
        qtd = quantidade if quantidade is not None else max(1, restante // 2)
        if qtd >= restante:
            raise ValueError("Execucao parcial deve manter quantidade remanescente.")
        self.registrar_execucao(qtd, preco_execucao)

    def executar(self, preco_execucao: float | None = None) -> None:
        if self.quantidade_remanescente <= 0:
            raise ValueError("A ordem ja foi totalmente executada.")
        self.registrar_execucao(self.quantidade_remanescente, preco_execucao)

    def rejeitar(self) -> None:
        if self._estado not in {EstadoOrdem.CRIADA, EstadoOrdem.ENVIADA}:
            raise ValueError("A ordem nao pode ser rejeitada neste estado.")
        self._estado = EstadoOrdem.REJEITADA

    def cancelar(self) -> None:
        if self._estado not in {EstadoOrdem.ENVIADA, EstadoOrdem.PARCIALMENTE_EXECUTADA}:
            raise ValueError("A ordem nao pode ser cancelada neste estado.")
        self._estado = EstadoOrdem.CANCELADA

    def atualizar(self, quantidade: int | None = None, preco: float | None = None) -> None:
        if self._estado not in {EstadoOrdem.CRIADA, EstadoOrdem.VALIDADA}:
            raise ValueError("A ordem nao pode ser atualizada neste estado.")
        if quantidade is not None:
            if quantidade <= 0:
                raise ValueError("A quantidade deve ser maior que zero.")
            if quantidade < self._quantidade_executada:
                raise ValueError("Quantidade nao pode ser menor que a ja executada.")
            self._quantidade = quantidade
        if preco is not None:
            if preco <= 0:
                raise ValueError("O preco limite deve ser maior que zero.")
            self._preco = preco
