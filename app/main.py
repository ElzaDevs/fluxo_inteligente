from fastapi import FastAPI

from app.schemas.solicitacao import SolicitacaoCreate


app = FastAPI(
    title="Sistema de Triagem e Priorização de Solicitações",
    description="API para organização, classificação e encaminhamento de solicitações internas.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "Sistema de Triagem de Solicitações está funcionando."
    }


@app.post("/solicitacoes")
def criar_solicitacao(solicitacao: SolicitacaoCreate):
    return {
        "mensagem": "Solicitação recebida com sucesso.",
        "solicitacao": solicitacao,
    }