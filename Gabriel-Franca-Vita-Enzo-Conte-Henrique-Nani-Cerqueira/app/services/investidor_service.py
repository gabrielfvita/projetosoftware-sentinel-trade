from app.repositories.investidor_repository import (
    InvestidorRepository
)

from app.security.password import gerar_hash_senha

from app.services.auditoria_service import (
    AuditoriaService
)


class InvestidorService:
    def __init__(
        self,
        repository: InvestidorRepository,
        auditoria_service: AuditoriaService
    ):
        self._repository = repository
        self._auditoria_service = auditoria_service

    def criar(
        self,
        nome: str,
        email: str,
        senha: str
    ):
        email = email.strip().lower()

        existente = self._repository.buscar_por_email(
            email
        )

        if existente is not None:
            raise ValueError(
                "E-mail já cadastrado."
            )

        senha_hash = gerar_hash_senha(
            senha
        )

        investidor = self._repository.criar(
            nome=nome.strip(),
            email=email,
            senha_hash=senha_hash
        )

        self._auditoria_service.registrar(
            evento="INVESTIDOR_CRIADO",
            resultado="SUCESSO",
            investidor_id=investidor.id
        )

        return investidor

    def consultar(
        self,
        investidor_id: int
    ):
        investidor = self._repository.buscar_por_id(
            investidor_id
        )

        if investidor is None:
            raise ValueError(
                "Investidor não encontrado."
            )

        return investidor

    def listar(self):
        return self._repository.listar()

    def atualizar(
        self,
        investidor_id: int,
        nome: str | None = None,
        email: str | None = None
    ):
        investidor = self.consultar(
            investidor_id
        )

        if nome is not None:
            investidor.nome = nome.strip()

        if email is not None:
            novo_email = email.strip().lower()

            existente = (
                self._repository.buscar_por_email(
                    novo_email
                )
            )

            if (
                existente is not None
                and existente.id != investidor_id
            ):
                raise ValueError(
                    "E-mail já cadastrado."
                )

            investidor.email = novo_email

        investidor = self._repository.atualizar(
            investidor
        )

        self._auditoria_service.registrar(
            evento="INVESTIDOR_ATUALIZADO",
            resultado="SUCESSO",
            investidor_id=investidor.id
        )

        return investidor

    def desativar(
        self,
        investidor_id: int
    ):
        investidor = self.consultar(
            investidor_id
        )

        investidor.status = "inativo"

        investidor = self._repository.atualizar(
            investidor
        )

        self._auditoria_service.registrar(
            evento="INVESTIDOR_DESATIVADO",
            resultado="SUCESSO",
            investidor_id=investidor.id
        )

        return investidor