import hashlib
import hmac
import os


ITERACOES = 200_000


def gerar_hash_senha(senha: str) -> str:
    if len(senha) < 8:
        raise ValueError(
            "A senha deve possuir pelo menos 8 caracteres."
        )

    salt = os.urandom(16)

    hash_senha = hashlib.pbkdf2_hmac(
        "sha256",
        senha.encode("utf-8"),
        salt,
        ITERACOES
    )

    return f"{salt.hex()}:{hash_senha.hex()}"


def verificar_senha(
    senha: str,
    senha_armazenada: str
) -> bool:
    try:
        salt_hex, hash_hex = senha_armazenada.split(":")

        salt = bytes.fromhex(salt_hex)

        hash_informado = hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            salt,
            ITERACOES
        )

        return hmac.compare_digest(
            hash_informado.hex(),
            hash_hex
        )

    except (ValueError, TypeError):
        return False