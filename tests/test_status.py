from app.rules.status import StatusSolicitacao, transicao_valida


def test_estados_de_espera_podem_pausar_e_retomar():
    assert transicao_valida(
        StatusSolicitacao.EM_PROCESSO,
        StatusSolicitacao.AGUARDANDO_SOLICITANTE,
    )
    assert transicao_valida(
        StatusSolicitacao.AGUARDANDO_SOLICITANTE,
        StatusSolicitacao.EM_PROCESSO,
    )

def test_aguardando_terceiro():
    assert transicao_valida(
        StatusSolicitacao.EM_PROCESSO,
        StatusSolicitacao.AGUARDANDO_TERCEIRO,
    )

def test_aguardando_aprovacao():
    assert transicao_valida(
        StatusSolicitacao.EM_ANALISE,
        StatusSolicitacao.AGUARDANDO_APROVACAO,
    )
