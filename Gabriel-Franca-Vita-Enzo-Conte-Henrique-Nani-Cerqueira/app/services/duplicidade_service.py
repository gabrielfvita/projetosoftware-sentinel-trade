import re


class DuplicidadeService:
    @staticmethod
    def validar_chave(chave: str) -> str:
        chave = chave.strip()

        if not re.fullmatch(r"[A-Za-z0-9_-]{8,64}", chave):
            raise ValueError(
                "Chave de idempotência inválida. "
                "Use entre 8 e 64 caracteres alfanuméricos, '-' ou '_'."
            )

        return chave