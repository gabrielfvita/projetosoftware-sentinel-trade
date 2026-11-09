from sqlalchemy import text

from app.database.database import engine


def criar_triggers_auditoria() -> None:
    with engine.begin() as conexao:
        conexao.execute(
            text(
                """
                CREATE TRIGGER IF NOT EXISTS impedir_update_auditoria
                BEFORE UPDATE ON registros_auditoria
                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Registros de auditoria são imutáveis'
                    );
                END;
                """
            )
        )

        conexao.execute(
            text(
                """
                CREATE TRIGGER IF NOT EXISTS impedir_delete_auditoria
                BEFORE DELETE ON registros_auditoria
                BEGIN
                    SELECT RAISE(
                        ABORT,
                        'Registros de auditoria são imutáveis'
                    );
                END;
                """
            )
        )