from datetime import datetime, timezone

from app.rules.prioridade import Prioridade
from app.rules.sla import (
    SlaSchedule,
    adicionar_tempo_sla,
    calcular_deadline,
    calcular_deadlines,
    calcular_sla_horas,
    obter_politica,
)


def test_politicas_de_sla():
    critica = obter_politica(Prioridade.CRITICA)
    alta = obter_politica(Prioridade.ALTA)
    media = obter_politica(Prioridade.MEDIA)
    baixa = obter_politica(Prioridade.BAIXA)

    assert (critica.resposta_minutos, critica.resolucao_minutos) == (15, 240)
    assert (alta.resposta_minutos, alta.resolucao_minutos) == (30, 480)
    assert (media.resposta_minutos, media.resolucao_minutos) == (240, 1440)
    assert (baixa.resposta_minutos, baixa.resolucao_minutos) == (480, 2400)

    assert critica.calendario == SlaSchedule.CONTINUO_24X7
    assert baixa.calendario == SlaSchedule.HORARIO_COMERCIAL


def test_compatibilidade_calcular_sla_horas():
    assert calcular_sla_horas(Prioridade.CRITICA) == 4
    assert calcular_sla_horas(Prioridade.ALTA) == 8
    assert calcular_sla_horas(Prioridade.MEDIA) == 24
    assert calcular_sla_horas(Prioridade.BAIXA) == 40


def test_sla_24x7():
    inicio = datetime(2026, 9, 26, 22, 0, tzinfo=timezone.utc)

    assert calcular_deadline(Prioridade.CRITICA, inicio) == datetime(
        2026, 9, 27, 2, 0, tzinfo=timezone.utc
    )


def test_sla_horario_comercial_pula_fora_do_expediente():
    inicio = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)

    assert adicionar_tempo_sla(
        inicio,
        240,
        SlaSchedule.HORARIO_COMERCIAL,
    ) == datetime(2026, 9, 28, 12, 0, tzinfo=timezone.utc)


def test_calcular_deadlines_retorna_resposta_e_resolucao():
    inicio = datetime(2026, 9, 26, 12, 0, tzinfo=timezone.utc)

    resposta, resolucao = calcular_deadlines(Prioridade.ALTA, inicio)

    assert resposta == datetime(2026, 9, 26, 12, 30, tzinfo=timezone.utc)
    assert resolucao == datetime(2026, 9, 26, 20, 0, tzinfo=timezone.utc)
