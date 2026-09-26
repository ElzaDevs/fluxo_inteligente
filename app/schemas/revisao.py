from pydantic import BaseModel, Field

from app.rules.prioridade import Impacto, Prioridade, Urgencia


class RevisaoSolicitacao(BaseModel):
    impacto: Impacto | None = None
    urgencia: Urgencia | None = None
    prioridade: Prioridade | None = None
    setor_responsavel: str | None = None
    justificativa: str = Field(min_length=10)
