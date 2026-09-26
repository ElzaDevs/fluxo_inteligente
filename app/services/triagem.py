from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.solicitacao import Solicitacao
from app.repositories.solicitacao import SolicitacaoRepository
from app.rules.encaminhamento import determinar_setor
from app.rules.prioridade import Impacto, Prioridade, Urgencia, determinar_prioridade
from app.rules.sla import calcular_deadlines, obter_politica
from app.schemas.solicitacao import SolicitacaoCreate
from app.models.usuario import Usuario


@dataclass(frozen=True)
class ResultadoTriagem:
    prioridade: Prioridade | None
    setor_responsavel: str | None
    sla_resposta_minutos: int | None
    sla_resolucao_minutos: int | None
    sla_response_deadline: datetime | None
    sla_deadline: datetime | None
    revisao_humana: bool
    motivo_revisao: str | None


def executar_triagem(
    solicitacao: Solicitacao,
    agora: datetime | None = None,
) -> ResultadoTriagem:
    impacto = Impacto(solicitacao.impacto_informado) if solicitacao.impacto_informado else None
    urgencia = Urgencia(solicitacao.urgencia_informada) if solicitacao.urgencia_informada else None
    setor = determinar_setor(solicitacao.categoria)
    motivos: list[str] = []

    if impacto is None or urgencia is None:
        motivos.append(
            "Impacto e/ou urgência não informados; classificação automática incompleta."
        )

    prioridade = (
        determinar_prioridade(impacto, urgencia)
        if impacto is not None and urgencia is not None
        else None
    )

    if setor is None:
        motivos.append("Não foi possível determinar o setor responsável pela categoria.")

    sla_resposta_minutos = None
    sla_resolucao_minutos = None
    sla_response_deadline = None
    sla_deadline = None

    if prioridade:
        politica = obter_politica(prioridade)
        sla_resposta_minutos = politica.resposta_minutos
        sla_resolucao_minutos = politica.resolucao_minutos
        sla_response_deadline, sla_deadline = calcular_deadlines(
            prioridade,
            agora,
        )

    solicitacao.impacto = impacto.value if impacto else None
    solicitacao.urgencia = urgencia.value if urgencia else None
    solicitacao.prioridade = prioridade.value if prioridade else None
    solicitacao.setor_responsavel = setor
    solicitacao.sla_resposta_minutos = sla_resposta_minutos
    solicitacao.sla_resolucao_minutos = sla_resolucao_minutos
    solicitacao.sla_response_deadline = sla_response_deadline
    solicitacao.sla_deadline = sla_deadline
    solicitacao.sla_status = "RUNNING" if prioridade else "PENDING_REVIEW"
    solicitacao.revisao_humana = bool(motivos)
    solicitacao.motivo_revisao = " ".join(motivos) if motivos else None

    return ResultadoTriagem(
        prioridade=prioridade,
        setor_responsavel=setor,
        sla_resposta_minutos=sla_resposta_minutos,
        sla_resolucao_minutos=sla_resolucao_minutos,
        sla_response_deadline=sla_response_deadline,
        sla_deadline=sla_deadline,
        revisao_humana=solicitacao.revisao_humana,
        motivo_revisao=solicitacao.motivo_revisao,
    )


def criar_solicitacao(db: Session, dados: SolicitacaoCreate, user: Usuario) -> Solicitacao:
    agora = datetime.now(timezone.utc)

    solicitacao = Solicitacao(
        empresa_id=user.empresa_id,
        titulo=dados.titulo,
        descricao=dados.descricao,
        solicitante=dados.solicitante,
        area_solicitante=dados.area_solicitante,
        categoria=dados.categoria,
        prazo=dados.prazo,
        evidencias=dados.evidencias,
        impacto_informado=dados.impacto_informado.value if dados.impacto_informado else None,
        urgencia_informada=dados.urgencia_informada.value if dados.urgencia_informada else None,
        status="ABERTA",
        created_at=agora,
        updated_at=agora,
    )

    resultado = executar_triagem(solicitacao, agora)
    repository = SolicitacaoRepository(db)
    repository.criar(solicitacao)

    repository.adicionar_historico(
        solicitacao,
        "TRIAGEM_AUTOMATICA",
        (
            "Triagem automática executada: "
            f"prioridade={resultado.prioridade.value if resultado.prioridade else 'não definida'}, "
            f"setor={resultado.setor_responsavel or 'não definido'}, "
            f"SLA_resposta={resultado.sla_resposta_minutos or 'não definido'} min, "
            f"SLA_resolucao={resultado.sla_resolucao_minutos or 'não definido'} min, "
            f"revisão_humana={'sim' if resultado.revisao_humana else 'não'}."
        ),
        agora,
    )

    return repository.salvar(solicitacao)
