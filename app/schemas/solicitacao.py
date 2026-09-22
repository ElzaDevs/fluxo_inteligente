from pydantic import BaseModel


class SolicitacaoCreate(BaseModel):
    titulo: str
    descricao: str
    area_solicitante: str
    prazo: str | None = None
    impacto_informado: str | None = None
    urgencia_informada: str | None = None