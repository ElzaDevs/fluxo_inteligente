import pytest

from app.rules.prioridade import (
    Impacto,
    Prioridade,
    Urgencia,
    determinar_prioridade,
)


@pytest.mark.parametrize(
    ("impacto", "urgencia", "prioridade_esperada"),
    [
        (Impacto.BAIXO, Urgencia.BAIXA, Prioridade.BAIXA),
        (Impacto.BAIXO, Urgencia.MEDIA, Prioridade.BAIXA),
        (Impacto.BAIXO, Urgencia.ALTA, Prioridade.MEDIA),
        (Impacto.BAIXO, Urgencia.CRITICA, Prioridade.ALTA),
        (Impacto.MEDIO, Urgencia.BAIXA, Prioridade.MEDIA),
        (Impacto.MEDIO, Urgencia.MEDIA, Prioridade.MEDIA),
        (Impacto.MEDIO, Urgencia.ALTA, Prioridade.ALTA),
        (Impacto.MEDIO, Urgencia.CRITICA, Prioridade.ALTA),
        (Impacto.ALTO, Urgencia.BAIXA, Prioridade.MEDIA),
        (Impacto.ALTO, Urgencia.MEDIA, Prioridade.MEDIA),
        (Impacto.ALTO, Urgencia.ALTA, Prioridade.ALTA),
        (Impacto.ALTO, Urgencia.CRITICA, Prioridade.CRITICA),
        (Impacto.CRITICO, Urgencia.BAIXA, Prioridade.ALTA),
        (Impacto.CRITICO, Urgencia.MEDIA, Prioridade.ALTA),
        (Impacto.CRITICO, Urgencia.ALTA, Prioridade.CRITICA),
        (Impacto.CRITICO, Urgencia.CRITICA, Prioridade.CRITICA),
    ],
)
def test_determinar_prioridade(impacto, urgencia, prioridade_esperada):
    assert determinar_prioridade(impacto, urgencia) == prioridade_esperada
