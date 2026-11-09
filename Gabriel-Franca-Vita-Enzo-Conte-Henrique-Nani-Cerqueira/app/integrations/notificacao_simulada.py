from app.integrations.interfaces import NotificacaoInterface


class ErroNotificacao(Exception):
    pass


class NotificacaoSimulada(NotificacaoInterface):
    def enviar(self, destinatario: str, mensagem: str) -> None:
        destinatario = (destinatario or "").strip()
        mensagem = (mensagem or "").strip()
        if not destinatario:
            raise ErroNotificacao("Destinatário de notificação inválido.")
        if not mensagem:
            raise ErroNotificacao("Mensagem de notificação inválida.")
        if len(mensagem) > 500:
            raise ErroNotificacao("Mensagem excede o tamanho permitido.")
        print(f"[NOTIFICACAO][{destinatario}] {mensagem}")
