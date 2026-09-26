from enum import Enum


class Impacto(str, Enum):
    BAIXO = "baixo"
    MEDIO = "medio"
    ALTO = "alto"
    CRITICO = "critico"


class Urgencia(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class Prioridade(str, Enum):
    CRITICA = "A"
    ALTA = "B"
    MEDIA = "C"
    BAIXA = "D"


MATRIZ_PRIORIDADE: dict[Impacto, dict[Urgencia, Prioridade]] = {
    Impacto.BAIXO: {
        Urgencia.BAIXA: Prioridade.BAIXA,
        Urgencia.MEDIA: Prioridade.BAIXA,
        Urgencia.ALTA: Prioridade.MEDIA,
        Urgencia.CRITICA: Prioridade.ALTA,
    },
    Impacto.MEDIO: {
        Urgencia.BAIXA: Prioridade.MEDIA,
        Urgencia.MEDIA: Prioridade.MEDIA,
        Urgencia.ALTA: Prioridade.ALTA,
        Urgencia.CRITICA: Prioridade.ALTA,
    },
    Impacto.ALTO: {
        Urgencia.BAIXA: Prioridade.MEDIA,
        Urgencia.MEDIA: Prioridade.MEDIA,
        Urgencia.ALTA: Prioridade.ALTA,
        Urgencia.CRITICA: Prioridade.CRITICA,
    },
    Impacto.CRITICO: {
        Urgencia.BAIXA: Prioridade.ALTA,
        Urgencia.MEDIA: Prioridade.ALTA,
        Urgencia.ALTA: Prioridade.CRITICA,
        Urgencia.CRITICA: Prioridade.CRITICA,
    },
}


def determinar_prioridade(
    impacto: Impacto,
    urgencia: Urgencia,
) -> Prioridade:
    """Determina a prioridade a partir da matriz impacto x urgência."""
    return MATRIZ_PRIORIDADE[impacto][urgencia]
