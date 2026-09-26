from enum import Enum


class StatusSolicitacao(str, Enum):
    ABERTA = "ABERTA"
    EM_ANALISE = "EM_ANALISE"
    EM_PROCESSO = "EM_PROCESSO"
    AGUARDANDO_SOLICITANTE = "AGUARDANDO_SOLICITANTE"
    AGUARDANDO_TERCEIRO = "AGUARDANDO_TERCEIRO"
    AGUARDANDO_APROVACAO = "AGUARDANDO_APROVACAO"
    SOLUCAO = "SOLUCAO"


STATUS_DE_ESPERA = {
    StatusSolicitacao.AGUARDANDO_SOLICITANTE,
    StatusSolicitacao.AGUARDANDO_TERCEIRO,
    StatusSolicitacao.AGUARDANDO_APROVACAO,
}


TRANSICOES_PERMITIDAS = {
    StatusSolicitacao.ABERTA: {StatusSolicitacao.EM_ANALISE},
    StatusSolicitacao.EM_ANALISE: {
        StatusSolicitacao.EM_PROCESSO,
        *STATUS_DE_ESPERA,
    },
    StatusSolicitacao.EM_PROCESSO: {
        StatusSolicitacao.SOLUCAO,
        *STATUS_DE_ESPERA,
    },
    StatusSolicitacao.AGUARDANDO_SOLICITANTE: {
        StatusSolicitacao.EM_PROCESSO,
    },
    StatusSolicitacao.AGUARDANDO_TERCEIRO: {
        StatusSolicitacao.EM_PROCESSO,
    },
    StatusSolicitacao.AGUARDANDO_APROVACAO: {
        StatusSolicitacao.EM_PROCESSO,
    },
}


def transicao_valida(atual: StatusSolicitacao, novo: StatusSolicitacao) -> bool:
    return novo in TRANSICOES_PERMITIDAS.get(atual, set())
