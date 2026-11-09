import hmac
import os


class MFAService:
    @staticmethod
    def codigo_controlado() -> str:
        return os.getenv(
            "MFA_TEST_CODE",
            "123456"
        )

    @classmethod
    def validar_codigo(
        cls,
        codigo: str
    ) -> bool:
        codigo_esperado = cls.codigo_controlado()

        return hmac.compare_digest(
            codigo,
            codigo_esperado
        )