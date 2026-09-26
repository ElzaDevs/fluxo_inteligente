from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Solicitacao(Base):
    __tablename__ = "solicitacoes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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

    sla_horas: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sla_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    revisao_humana: Mapped[bool] = mapped_column(Boolean, default=False)
    motivo_revisao: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str] = mapped_column(String(30), default="ABERTA")
    solucao: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    historico: Mapped[list["HistoricoSolicitacao"]] = relationship(
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

    solicitacao: Mapped[Solicitacao] = relationship(back_populates="historico")
