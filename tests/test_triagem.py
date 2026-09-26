from datetime import datetime, timezone
from types import SimpleNamespace

from app.services.triagem import executar_triagem


def solicitacao(**kwargs):
    dados = {
        "impacto_informado": "critico",
        "urgencia_informada": "critica",
        "categoria": "TI / Sistemas",
    }
    dados.update(kwargs)

    return SimpleNamespace(
        impacto_informado=dados["impacto_informado"],
        urgencia_informada=dados["urgencia_informada"],
        categoria=dados["categoria"],
        impacto=None,
        urgencia=None,
        prioridade=None,
        setor_responsavel=None,
        sla_horas=None,
        sla_deadline=None,
        revisao_humana=False,
        motivo_revisao=None,
    )


def test_triagem_critica_completa():
    resultado = executar_triagem(
        solicitacao(),
        datetime(2026, 9, 26, 12, 0, tzinfo=timezone.utc),
    )
    assert resultado.prioridade.value == "A"
    assert resultado.setor_responsavel == "Tecnologia da Informação"
    assert resultado.sla_horas == 2
    assert resultado.revisao_humana is False


def test_triagem_sem_impacto_exige_revisao():
    resultado = executar_triagem(
        solicitacao(impacto_informado=None),
        datetime(2026, 9, 26, 12, 0, tzinfo=timezone.utc),
    )
    assert resultado.prioridade is None
    assert resultado.revisao_humana is True
    assert resultado.motivo_revisao


def test_categoria_desconhecida_exige_revisao():
    resultado = executar_triagem(
        solicitacao(categoria="Juridico"),
        datetime(2026, 9, 26, 12, 0, tzinfo=timezone.utc),
    )
    assert resultado.prioridade.value == "A"
    assert resultado.revisao_humana is True
    assert resultado.setor_responsavel is None
