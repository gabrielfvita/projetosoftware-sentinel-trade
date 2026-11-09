import time


class RateLimitService:
    MAX_TENTATIVAS = 5
    JANELA_SEGUNDOS = 60

    _tentativas: dict[str, list[float]] = {}

    @classmethod
    def verificar(cls, identificador: str) -> None:
        agora = time.monotonic()

        tentativas = cls._tentativas.get(
            identificador,
            []
        )

        tentativas_validas = [
            instante
            for instante in tentativas
            if agora - instante < cls.JANELA_SEGUNDOS
        ]

        cls._tentativas[identificador] = tentativas_validas

        if len(tentativas_validas) >= cls.MAX_TENTATIVAS:
            raise ValueError(
                "Muitas tentativas. Tente novamente mais tarde."
            )

    @classmethod
    def registrar_falha(cls, identificador: str) -> None:
        agora = time.monotonic()

        if identificador not in cls._tentativas:
            cls._tentativas[identificador] = []

        cls._tentativas[identificador].append(
            agora
        )

    @classmethod
    def limpar(cls, identificador: str) -> None:
        cls._tentativas.pop(
            identificador,
            None
        )