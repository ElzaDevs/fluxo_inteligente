from datetime import datetime, timezone

from app.rules.prioridade import Prioridade
from app.rules.sla import calcular_deadline, calcular_sla_horas


def test_sla_por_prioridade():
    assert calcular_sla_horas(Prioridade.CRITICA) == 2
    assert calcular_sla_horas(Prioridade.ALTA) == 8
    assert calcular_sla_horas(Prioridade.MEDIA) == 24
    assert calcular_sla_horas(Prioridade.BAIXA) == 72


def test_deadline_respeita_sla():
    inicio = datetime(2026, 9, 26, 12, 0, tzinfo=timezone.utc)
    assert calcular_deadline(Prioridade.ALTA, inicio) == datetime(
        2026, 9, 26, 20, 0, tzinfo=timezone.utc
    )
