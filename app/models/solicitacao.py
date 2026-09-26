from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    titulo: Mapped[str] = mapped_column(String(160))
    descricao: Mapped[str] = mapped_column(Text)
    solicitante: Mapped[str] = mapped_column(String(120))
    area_solicitante: Mapped[str] = mapped_column(String(120))
    categoria: Mapped[str] = mapped_column(String(80))

    prazo: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    evidencias: Mapped[str | None] = mapped_column(Text, nullable=True)

    impacto_informado: Mapped[str | None] = mapped_column(String(20), nullable=True)
    urgencia_informada: Mapped[str | None] = mapped_column(String(20), nullable=True)

    impacto: Mapped[str | None] = mapped_column(String(20), nullable=True)
    urgencia: Mapped[str | None] = mapped_column(String(20), nullable=True)
    prioridade: Mapped[str | None] = mapped_column(String(1), nullable=True)
    setor_responsavel: Mapped[str | None] = mapped_column(String(120), nullable=True)

    sla_resposta_minutos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sla_resolucao_minutos: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sla_response_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sla_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sla_status: Mapped[str] = mapped_column(String(20), default="RUNNING")
    sla_paused_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    sla_paused_minutes: Mapped[int] = mapped_column(Integer, default=0)

    revisao_humana: Mapped[bool] = mapped_column(Boolean, default=False)
    motivo_revisao: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(30), default="ABERTA")
    solucao: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    empresa = relationship("Empresa", back_populates="solicitacoes")
    historico = relationship(
        "HistoricoSolicitacao",
        back_populates="solicitacao",
        cascade="all, delete-orphan",
        order_by="HistoricoSolicitacao.criado_em",
    )


class HistoricoSolicitacao(Base):
    __tablename__ = "historico_solicitacoes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    solicitacao_id: Mapped[int] = mapped_column(ForeignKey("solicitacoes.id"))
    tipo_evento: Mapped[str] = mapped_column(String(50))
    descricao: Mapped[str] = mapped_column(Text)
    criado_em: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    solicitacao = relationship("Solicitacao", back_populates="historico")
