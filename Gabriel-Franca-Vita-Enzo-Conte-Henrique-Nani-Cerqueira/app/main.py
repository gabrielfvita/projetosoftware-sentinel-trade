from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.api.ativos import router as ativos_router
from app.api.auth import router as auth_router
from app.api.carteira import router as carteira_router
from app.api.contas import router as contas_router
from app.api.historico import router as historico_router
from app.api.investidores import router as investidores_router
from app.api.ordens import router as ordens_router

from app.database.database import Base, engine
from app.database import models
from app.database.auditoria_triggers import (
    criar_triggers_auditoria
)


Base.metadata.create_all(
    bind=engine
)

criar_triggers_auditoria()


app = FastAPI(
    title="SentinelTrade",
    description=(
        "Plataforma simulada para gerenciamento "
        "e execução de ordens financeiras."
    ),
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(investidores_router)
app.include_router(contas_router)
app.include_router(carteira_router)
app.include_router(ativos_router)
app.include_router(ordens_router)
app.include_router(historico_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "SentinelTrade"
    }