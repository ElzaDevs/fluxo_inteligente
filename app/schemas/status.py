from pydantic import BaseModel, Field

from app.rules.status import StatusSolicitacao


class AtualizacaoStatus(BaseModel):
    status: StatusSolicitacao
    solucao: str | None = Field(default=None, min_length=5)
