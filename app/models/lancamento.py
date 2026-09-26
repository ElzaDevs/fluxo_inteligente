from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class LancamentoFinanceiro(Base):
    __tablename__ = "lancamentos_financeiros"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), index=True)
    criado_por_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    tipo: Mapped[str] = mapped_column(String(10))
    descricao: Mapped[str] = mapped_column(String(180))
    categoria: Mapped[str] = mapped_column(String(80), index=True)
    valor: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    data_lancamento: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(20), default="REALIZADO")
    observacoes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    empresa = relationship("Empresa", back_populates="lancamentos")
    criado_por = relationship("Usuario", back_populates="lancamentos")
