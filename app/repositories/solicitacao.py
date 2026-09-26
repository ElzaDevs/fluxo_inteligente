from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.solicitacao import HistoricoSolicitacao, Solicitacao


class SolicitacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, solicitacao: Solicitacao) -> Solicitacao:
        self.db.add(solicitacao)
        self.db.flush()
        return solicitacao

    def buscar(self, solicitacao_id: int) -> Solicitacao | None:
        return self.db.scalar(
            select(Solicitacao).where(Solicitacao.id == solicitacao_id)
        )

    def listar(self, limit: int = 100) -> list[Solicitacao]:
        return list(
            self.db.scalars(
                select(Solicitacao)
                .order_by(Solicitacao.created_at.desc())
                .limit(limit)
            ).all()
        )

    def adicionar_historico(
        self,
        solicitacao: Solicitacao,
        tipo_evento: str,
        descricao: str,
        criado_em: datetime,
    ) -> HistoricoSolicitacao:
        evento = HistoricoSolicitacao(
            solicitacao=solicitacao,
            tipo_evento=tipo_evento,
            descricao=descricao,
            criado_em=criado_em,
        )
        self.db.add(evento)
        return evento

    def salvar(self, solicitacao: Solicitacao) -> Solicitacao:
        self.db.add(solicitacao)
        self.db.commit()
        self.db.refresh(solicitacao)
        return solicitacao
