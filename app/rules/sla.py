from dataclasses import dataclass
from datetime import datetime, timedelta, time, timezone
from enum import Enum

from app.rules.prioridade import Prioridade


class SlaSchedule(str, Enum):
    CONTINUO_24X7 = "24x7"
    HORARIO_COMERCIAL = "business_hours"


@dataclass(frozen=True)
class SlaPolitica:
    prioridade: Prioridade
    resposta_minutos: int
    resolucao_minutos: int
    calendario: SlaSchedule


SLA_POLITICAS: dict[Prioridade, SlaPolitica] = {
    Prioridade.CRITICA: SlaPolitica(
        prioridade=Prioridade.CRITICA,
        resposta_minutos=15,
        resolucao_minutos=4 * 60,
        calendario=SlaSchedule.CONTINUO_24X7,
    ),
    Prioridade.ALTA: SlaPolitica(
        prioridade=Prioridade.ALTA,
        resposta_minutos=30,
        resolucao_minutos=8 * 60,
        calendario=SlaSchedule.CONTINUO_24X7,
    ),
    Prioridade.MEDIA: SlaPolitica(
        prioridade=Prioridade.MEDIA,
        resposta_minutos=4 * 60,
        resolucao_minutos=24 * 60,
        calendario=SlaSchedule.HORARIO_COMERCIAL,
    ),
    Prioridade.BAIXA: SlaPolitica(
        prioridade=Prioridade.BAIXA,
        resposta_minutos=8 * 60,
        resolucao_minutos=40 * 60,
        calendario=SlaSchedule.HORARIO_COMERCIAL,
    ),
}

INICIO_EXPEDIENTE = time(9, 0)
FIM_EXPEDIENTE = time(18, 0)
INICIO_INTERVALO = time(12, 0)
FIM_INTERVALO = time(13, 0)


def obter_politica(prioridade: Prioridade) -> SlaPolitica:
    return SLA_POLITICAS[prioridade]


def calcular_sla_horas(prioridade: Prioridade) -> int:
    """Mantém compatibilidade: retorna o alvo de resolução em horas."""
    return obter_politica(prioridade).resolucao_minutos // 60


def _minuto_util_comercial(moment: datetime) -> bool:
    if moment.weekday() >= 5:
        return False
    hora = moment.time()
    return (
        INICIO_EXPEDIENTE <= hora < INICIO_INTERVALO
        or FIM_INTERVALO <= hora < FIM_EXPEDIENTE
    )


def _proximo_minuto_comercial(moment: datetime) -> datetime:
    cursor = moment.replace(second=0, microsecond=0)
    if cursor.weekday() >= 5:
        dias = 7 - cursor.weekday()
        return (cursor + timedelta(days=dias)).replace(
            hour=9, minute=0, second=0, microsecond=0
        )
    if cursor.time() < INICIO_EXPEDIENTE:
        return cursor.replace(hour=9, minute=0, second=0, microsecond=0)
    if INICIO_INTERVALO <= cursor.time() < FIM_INTERVALO:
        return cursor.replace(hour=13, minute=0, second=0, microsecond=0)
    if cursor.time() >= FIM_EXPEDIENTE:
        return (cursor + timedelta(days=1)).replace(
            hour=9, minute=0, second=0, microsecond=0
        )
    return cursor


def adicionar_tempo_sla(
    inicio: datetime,
    minutos: int,
    calendario: SlaSchedule,
) -> datetime:
    if calendario == SlaSchedule.CONTINUO_24X7:
        return inicio + timedelta(minutes=minutos)

    cursor = _proximo_minuto_comercial(inicio)
    restante = minutos

    while restante > 0:
        if not _minuto_util_comercial(cursor):
            cursor = _proximo_minuto_comercial(cursor)
            continue

        cursor += timedelta(minutes=1)
        restante -= 1

    return cursor


def calcular_deadline(
    prioridade: Prioridade,
    inicio: datetime | None = None,
) -> datetime:
    base = inicio or datetime.now(timezone.utc)
    politica = obter_politica(prioridade)
    return adicionar_tempo_sla(
        base,
        politica.resolucao_minutos,
        politica.calendario,
    )


def calcular_deadlines(
    prioridade: Prioridade,
    inicio: datetime | None = None,
) -> tuple[datetime, datetime]:
    base = inicio or datetime.now(timezone.utc)
    politica = obter_politica(prioridade)
    return (
        adicionar_tempo_sla(base, politica.resposta_minutos, politica.calendario),
        adicionar_tempo_sla(base, politica.resolucao_minutos, politica.calendario),
    )
