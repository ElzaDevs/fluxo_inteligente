from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(160))
    cnpj: Mapped[str | None] = mapped_column(String(18), unique=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    usuarios = relationship("Usuario", back_populates="empresa", cascade="all, delete-orphan")
    lancamentos = relationship(
        "LancamentoFinanceiro",
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
    solicitacoes = relationship(
        "Solicitacao",
        back_populates="empresa",
        cascade="all, delete-orphan",
    )
