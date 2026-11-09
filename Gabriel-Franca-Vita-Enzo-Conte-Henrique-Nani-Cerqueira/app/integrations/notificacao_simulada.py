from app.integrations.interfaces import NotificacaoInterface


class ErroNotificacao(Exception):
    pass


class NotificacaoSimulada(NotificacaoInterface):

    def enviar(
        self,
        mensagem: str
    ) -> None:
        if not mensagem:
            raise ErroNotificacao(
                "Mensagem de notificação inválida."
            )

        mensagem = mensagem.strip()

        if len(mensagem) > 500:
            raise ErroNotificacao(
                "Mensagem excede o tamanho permitido."
            )

        try:
            print(
                f"[NOTIFICACAO] {mensagem}"
            )

        except Exception as erro:
            raise ErroNotificacao(
                "Falha no serviço externo de notificação."
            ) from erro