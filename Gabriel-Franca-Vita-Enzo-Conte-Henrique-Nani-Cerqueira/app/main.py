from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.ordens import router as ordens_router
from app.database.database import Base, engine
from app.database import models


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="SentinelTrade",
    description=(
        "Plataforma simulada para gerenciamento "
        "e execução de ordens financeiras."
    ),
    version="1.0.0"
)


app.include_router(
    auth_router
)

app.include_router(
    ordens_router
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "SentinelTrade"
    }