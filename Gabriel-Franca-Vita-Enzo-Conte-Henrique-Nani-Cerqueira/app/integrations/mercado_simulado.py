class MercadoSimulado:
    def __init__(self, aberto: bool = True):
        self._aberto = aberto

    def esta_aberto(self) -> bool:
        return self._aberto

    def abrir(self) -> None:
        self._aberto = True

    def fechar(self) -> None:
        self._aberto = False