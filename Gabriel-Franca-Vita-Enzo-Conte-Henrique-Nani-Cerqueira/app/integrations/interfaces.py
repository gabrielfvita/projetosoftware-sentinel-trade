from abc import ABC, abstractmethod

from app.domain.ativo import Ativo


class BolsaInterface(ABC):
    @abstractmethod
    def processar_ordem(self, ordem, cotacao: float):
        pass


class CotacaoInterface(ABC):
    @abstractmethod
    def consultar(self, ativo: Ativo, timeout_segundos: float = 2.0) -> float:
        pass


class NotificacaoInterface(ABC):
    @abstractmethod
    def enviar(self, destinatario: str, mensagem: str) -> None:
        pass
