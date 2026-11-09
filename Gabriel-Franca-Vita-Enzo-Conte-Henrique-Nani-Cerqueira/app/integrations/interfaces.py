from abc import ABC, abstractmethod

from app.domain.ativo import Ativo
from app.domain.ordem import Ordem


class BolsaInterface(ABC):

    @abstractmethod
    def processar_ordem(self):
        pass


class CotacaoInterface(ABC):

    @abstractmethod
    def consultar(
        self,
        ativo: Ativo,
        timeout_segundos: float = 2.0
    ) -> float:
        pass


class NotificacaoInterface(ABC):

    @abstractmethod
    def enviar(
        self,
        mensagem: str
    ) -> None:
        pass