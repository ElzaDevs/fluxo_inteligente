from datetime import date, datetime
from decimal import Decimal
from typing import Any, Literal

from pydantic import BaseModel, Field, field_serializer


TipoLancamento = Literal["RECEITA", "DESPESA"]
StatusLancamento = Literal["REALIZADO", "PENDENTE"]


class LancamentoCreate(BaseModel):
    tipo: TipoLancamento
    descricao: str = Field(min_length=2, max_length=180)
    categoria: str = Field(min_length=2, max_length=80)
    valor: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    data_lancamento: date
    status: StatusLancamento = "REALIZADO"
    observacoes: str | None = None


class LancamentoUpdate(BaseModel):
    tipo: TipoLancamento | None = None
    descricao: str | None = Field(default=None, min_length=2, max_length=180)
    categoria: str | None = Field(default=None, min_length=2, max_length=80)
    valor: Decimal | None = Field(default=None, gt=0, max_digits=14, decimal_places=2)
    data_lancamento: date | None = None
    status: StatusLancamento | None = None
    observacoes: str | None = None


class FinanceiroResponseModel(BaseModel):
    @field_serializer("*", when_used="json")
    def serialize_decimal_values(self, value: Any) -> Any:
        if isinstance(value, Decimal):
            return float(value)
        return value


class LancamentoResponse(FinanceiroResponseModel):
    id: int
    tipo: TipoLancamento
    descricao: str
    categoria: str
    valor: Decimal
    data_lancamento: date
    status: StatusLancamento
    observacoes: str | None
    created_at: datetime


class CategoriaResumo(FinanceiroResponseModel):
    categoria: str
    total: Decimal


class MesResumo(FinanceiroResponseModel):
    mes: str
    receitas: Decimal
    despesas: Decimal


class DashboardResponse(FinanceiroResponseModel):
    periodo_inicio: date
    periodo_fim: date
    total_receitas: Decimal
    total_despesas: Decimal
    saldo: Decimal
    receitas_pendentes: Decimal
    despesas_pendentes: Decimal
    quantidade_lancamentos: int
    despesas_por_categoria: list[CategoriaResumo]
    evolucao_mensal: list[MesResumo]
    recentes: list[LancamentoResponse]
