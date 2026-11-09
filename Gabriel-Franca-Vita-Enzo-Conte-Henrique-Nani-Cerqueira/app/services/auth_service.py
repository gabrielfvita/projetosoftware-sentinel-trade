from app.repositories.investidor_repository import (
    InvestidorRepository
)

from app.security.mfa import MFAService
from app.security.password import verificar_senha
from app.security.rate_limit import RateLimitService

from app.services.auditoria_service import (
    AuditoriaService
)


class AuthService:
    def __init__(
        self,
        repository: InvestidorRepository,
        auditoria_service: AuditoriaService
    ):
        self._repository = repository
        self._auditoria_service = auditoria_service

    def autenticar_senha(
        self,
        email: str,
        senha: str
    ):
        identificador = email.strip().lower()

        RateLimitService.verificar(
            identificador
        )

        investidor = self._repository.buscar_por_email(
            identificador
        )

        if investidor is None:
            RateLimitService.registrar_falha(
                identificador
            )

            self._auditoria_service.registrar(
                evento="LOGIN_FALHOU",
                resultado="CREDENCIAIS_INVALIDAS"
            )

            raise ValueError(
                "Credenciais inválidas."
            )

        if investidor.status != "ativo":
            RateLimitService.registrar_falha(
                identificador
            )

            self._auditoria_service.registrar(
                evento="LOGIN_FALHOU",
                resultado="USUARIO_INATIVO",
                investidor_id=investidor.id
            )

            raise ValueError(
                "Credenciais inválidas."
            )

        if not verificar_senha(
            senha,
            investidor.senha_hash
        ):
            RateLimitService.registrar_falha(
                identificador
            )

            self._auditoria_service.registrar(
                evento="LOGIN_FALHOU",
                resultado="CREDENCIAIS_INVALIDAS",
                investidor_id=investidor.id
            )

            raise ValueError(
                "Credenciais inválidas."
            )

        RateLimitService.limpar(
            identificador
        )

        self._auditoria_service.registrar(
            evento="SENHA_VALIDADA",
            resultado="SUCESSO",
            investidor_id=investidor.id
        )

        return investidor

    def validar_mfa(
        self,
        investidor_id: int,
        codigo: str
    ) -> bool:
        investidor = self._repository.buscar_por_id(
            investidor_id
        )

        if investidor is None:
            raise ValueError(
                "Investidor não encontrado."
            )

        if not investidor.mfa_habilitado:
            self._auditoria_service.registrar(
                evento="MFA",
                resultado="NAO_HABILITADO",
                investidor_id=investidor.id
            )

            return True

        if not MFAService.validar_codigo(
            codigo
        ):
            self._auditoria_service.registrar(
                evento="MFA_FALHOU",
                resultado="CODIGO_INVALIDO",
                investidor_id=investidor.id
            )

            raise ValueError(
                "Código MFA inválido."
            )

        self._auditoria_service.registrar(
            evento="MFA_VALIDADO",
            resultado="SUCESSO",
            investidor_id=investidor.id
        )

        return True