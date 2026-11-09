from sqlalchemy import inspect, text

from app.database.database import engine


def executar_migracoes() -> None:
    inspetor = inspect(engine)
    if "ordens" not in inspetor.get_table_names():
        return

    colunas = {coluna["name"] for coluna in inspetor.get_columns("ordens")}
    with engine.begin() as conexao:
        if "quantidade_executada" not in colunas:
            conexao.execute(text(
                "ALTER TABLE ordens ADD COLUMN quantidade_executada INTEGER NOT NULL DEFAULT 0"
            ))
        if "preco_medio_execucao" not in colunas:
            conexao.execute(text(
                "ALTER TABLE ordens ADD COLUMN preco_medio_execucao FLOAT NULL"
            ))
