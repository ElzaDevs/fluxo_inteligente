from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import app.models  # noqa: F401
from app.api.auth import router as auth_router
from app.api.financeiro import router as financeiro_router
from app.api.solicitacoes import router as solicitacoes_router
from app.api.web import router as web_router
from app.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fluxo Inteligente",
    description=(
        "Sistema web multiempresa para gestão financeira e triagem de "
        "solicitações, com regras de negócio, SLA, autenticação e rastreabilidade."
    ),
    version="2.0.0",
)

static_dir = Path("static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(web_router)
app.include_router(auth_router)
app.include_router(financeiro_router)
app.include_router(solicitacoes_router)


@app.get("/health", tags=["Sistema"])
def health():
    return {"status": "ok", "service": "fluxo-inteligente"}
