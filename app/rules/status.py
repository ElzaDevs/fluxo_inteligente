from enum import Enum


class StatusSolicitacao(str, Enum):
    ABERTA = "ABERTA"
    EM_ANALISE = "EM_ANALISE"
    EM_PROCESSO = "EM_PROCESSO"
    SOLUCAO = "SOLUCAO"


TRANSICOES_PERMITIDAS: dict[StatusSolicitacao, set[StatusSolicitacao]] = {
    StatusSolicitacao.ABERTA: {StatusSolicitacao.EM_ANALISE},
    StatusSolicitacao.EM_ANALISE: {StatusSolicitacao.EM_PROCESSO},
    StatusSolicitacao.EM_PROCESSO: {StatusSolicitacao.SOLUCAO},
}


def transicao_valida(atual: StatusSolicitacao, novo: StatusSolicitacao) -> bool:
    return novo in TRANSICOES_PERMITIDAS.get(atual, set())
