from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.rules.prioridade import Impacto, Prioridade, Urgencia
from app.rules.status import StatusSolicitacao


class SolicitacaoCreate(BaseModel):
    titulo: str = Field(min_length=3, max_length=160)
    descricao: str = Field(min_length=10)
    solicitante: str = Field(min_length=2, max_length=120)
    area_solicitante: str = Field(min_length=2, max_length=120)
    categoria: str = Field(min_length=2, max_length=80)
    prazo: datetime | None = None
    evidencias: str | None = None
    impacto_informado: Impacto | None = None
    urgencia_informada: Urgencia | None = None


class HistoricoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tipo_evento: str
    descricao: str
    criado_em: datetime


class SolicitacaoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descricao: str
    solicitante: str
    area_solicitante: str
    categoria: str
    prazo: datetime | None

    impacto: Impacto | None
    urgencia: Urgencia | None
    prioridade: Prioridade | None
    setor_responsavel: str | None

    sla_horas: int | None
    sla_deadline: datetime | None
    revisao_humana: bool
    motivo_revisao: str | None
    status: StatusSolicitacao
    solucao: str | None

    created_at: datetime
    updated_at: datetime
    historico: list[HistoricoResponse] = Field(default_factory=list)


class SolicitacaoListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    prioridade: Prioridade | None
    setor_responsavel: str | None
    status: StatusSolicitacao
    revisao_humana: bool
    created_at: datetime
