from datetime import datetime, timedelta, timezone

from app.rules.prioridade import Prioridade


SLA_HORAS: dict[Prioridade, int] = {
    Prioridade.CRITICA: 2,
    Prioridade.ALTA: 8,
    Prioridade.MEDIA: 24,
    Prioridade.BAIXA: 72,
}


def calcular_sla_horas(prioridade: Prioridade) -> int:
    return SLA_HORAS[prioridade]


def calcular_deadline(
    prioridade: Prioridade,
    inicio: datetime | None = None,
) -> datetime:
    base = inicio or datetime.now(timezone.utc)
    return base + timedelta(hours=calcular_sla_horas(prioridade))
