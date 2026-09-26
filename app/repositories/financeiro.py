from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lancamento import LancamentoFinanceiro


class FinanceiroRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, lancamento: LancamentoFinanceiro) -> LancamentoFinanceiro:
        self.db.add(lancamento)
        self.db.flush()
        return lancamento

    def buscar(self, empresa_id: int, lancamento_id: int) -> LancamentoFinanceiro | None:
        return self.db.scalar(
            select(LancamentoFinanceiro).where(
                LancamentoFinanceiro.id == lancamento_id,
                LancamentoFinanceiro.empresa_id == empresa_id,
            )
        )

    def listar(
        self,
        empresa_id: int,
        inicio: date | None = None,
        fim: date | None = None,
    ) -> list[LancamentoFinanceiro]:
        query = select(LancamentoFinanceiro).where(
            LancamentoFinanceiro.empresa_id == empresa_id
        )
        if inicio:
            query = query.where(LancamentoFinanceiro.data_lancamento >= inicio)
        if fim:
            query = query.where(LancamentoFinanceiro.data_lancamento <= fim)

        return list(
            self.db.scalars(
                query.order_by(LancamentoFinanceiro.data_lancamento.desc(), LancamentoFinanceiro.id.desc())
            ).all()
        )

    def excluir(self, lancamento: LancamentoFinanceiro) -> None:
        self.db.delete(lancamento)
        self.db.commit()

    def salvar(self, lancamento: LancamentoFinanceiro) -> LancamentoFinanceiro:
        self.db.add(lancamento)
        self.db.commit()
        self.db.refresh(lancamento)
        return lancamento
