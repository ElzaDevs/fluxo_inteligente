from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_csrf
from app.models.usuario import Usuario
from app.repositories.solicitacao import SolicitacaoRepository
from app.rules.prioridade import Impacto, Prioridade, Urgencia, determinar_prioridade
from app.rules.sla import calcular_deadlines, obter_politica
from app.rules.status import STATUS_DE_ESPERA, StatusSolicitacao, transicao_valida
from app.schemas.revisao import RevisaoSolicitacao
from app.schemas.solicitacao import SolicitacaoCreate, SolicitacaoListItem, SolicitacaoResponse
from app.schemas.status import AtualizacaoStatus
from app.services.triagem import criar_solicitacao

router = APIRouter(prefix="/solicitacoes", tags=["Triagem"])


@router.post("", response_model=SolicitacaoResponse, status_code=status.HTTP_201_CREATED)
def criar(
    dados: SolicitacaoCreate,
    user: Usuario = Depends(require_csrf),
    db: Session = Depends(get_db),
):
    return criar_solicitacao(db, dados, user)


@router.get("", response_model=list[SolicitacaoListItem])
def listar(
    limit: int = Query(default=100, ge=1, le=100),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return SolicitacaoRepository(db).listar(user.empresa_id, limit=limit)


@router.get("/{solicitacao_id}", response_model=SolicitacaoResponse)
def detalhar(
    solicitacao_id: int,
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    solicitacao = SolicitacaoRepository(db).buscar(user.empresa_id, solicitacao_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
    return solicitacao


@router.patch("/{solicitacao_id}/revisao", response_model=SolicitacaoResponse)
def revisar(
    solicitacao_id: int,
    dados: RevisaoSolicitacao,
    user: Usuario = Depends(require_csrf),
    db: Session = Depends(get_db),
):
    repository = SolicitacaoRepository(db)
    solicitacao = repository.buscar(user.empresa_id, solicitacao_id)

    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

    impacto = dados.impacto.value if dados.impacto else solicitacao.impacto
    urgencia = dados.urgencia.value if dados.urgencia else solicitacao.urgencia
    setor = dados.setor_responsavel or solicitacao.setor_responsavel

    if not impacto or not urgencia or not setor:
        raise HTTPException(
            status_code=422,
            detail="A revisão deve definir impacto, urgência e setor responsável.",
        )

    prioridade = (
        dados.prioridade
        if dados.prioridade
        else determinar_prioridade(Impacto(impacto), Urgencia(urgencia))
    )

    agora = datetime.now(timezone.utc)
    politica = obter_politica(prioridade)
    response_deadline, resolution_deadline = calcular_deadlines(
        prioridade,
        solicitacao.created_at,
    )

    solicitacao.impacto = impacto
    solicitacao.urgencia = urgencia
    solicitacao.prioridade = prioridade.value
    solicitacao.setor_responsavel = setor
    solicitacao.sla_resposta_minutos = politica.resposta_minutos
    solicitacao.sla_resolucao_minutos = politica.resolucao_minutos
    solicitacao.sla_response_deadline = response_deadline
    solicitacao.sla_deadline = resolution_deadline
    solicitacao.sla_status = "RUNNING"
    solicitacao.revisao_humana = False
    solicitacao.motivo_revisao = None
    solicitacao.updated_at = agora

    repository.adicionar_historico(
        solicitacao,
        "REVISAO_HUMANA",
        (
            f"{dados.justificativa} "
            f"Prioridade revisada para {prioridade.value}; "
            f"setor responsável: {setor}."
        ),
        agora,
    )

    return repository.salvar(solicitacao)


@router.patch("/{solicitacao_id}/status", response_model=SolicitacaoResponse)
def atualizar_status(
    solicitacao_id: int,
    dados: AtualizacaoStatus,
    user: Usuario = Depends(require_csrf),
    db: Session = Depends(get_db),
):
    repository = SolicitacaoRepository(db)
    solicitacao = repository.buscar(user.empresa_id, solicitacao_id)

    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

    atual = StatusSolicitacao(solicitacao.status)

    if not transicao_valida(atual, dados.status):
        raise HTTPException(
            status_code=409,
            detail=f"Transição inválida: {atual.value} -> {dados.status.value}.",
        )

    if dados.status == StatusSolicitacao.SOLUCAO and not dados.solucao:
        raise HTTPException(
            status_code=422,
            detail="A solução é obrigatória ao concluir uma solicitação.",
        )

    agora = datetime.now(timezone.utc)
    entrando_em_espera = dados.status in STATUS_DE_ESPERA
    saindo_de_espera = atual in STATUS_DE_ESPERA and dados.status == StatusSolicitacao.EM_PROCESSO

    if entrando_em_espera:
        solicitacao.sla_paused_at = agora
        solicitacao.sla_status = "PAUSED"

    if saindo_de_espera:
        if solicitacao.sla_paused_at:
            pausa = agora - solicitacao.sla_paused_at
            minutos_pausa = max(0, int(pausa.total_seconds() // 60))
            solicitacao.sla_paused_minutes += minutos_pausa
            if solicitacao.sla_response_deadline:
                solicitacao.sla_response_deadline += pausa
            if solicitacao.sla_deadline:
                solicitacao.sla_deadline += pausa

        solicitacao.sla_paused_at = None
        solicitacao.sla_status = "RUNNING"

    if dados.status == StatusSolicitacao.SOLUCAO:
        solicitacao.sla_status = (
            "MET"
            if solicitacao.sla_deadline and agora <= solicitacao.sla_deadline
            else "BREACHED"
        )

    solicitacao.status = dados.status.value
    solicitacao.updated_at = agora

    if dados.solucao:
        solicitacao.solucao = dados.solucao

    repository.adicionar_historico(
        solicitacao,
        "MUDANCA_STATUS",
        f"Status alterado de {atual.value} para {dados.status.value}.",
        agora,
    )

    if entrando_em_espera:
        repository.adicionar_historico(
            solicitacao,
            "SLA_PAUSADO",
            f"SLA pausado em {dados.status.value}.",
            agora,
        )

    if saindo_de_espera:
        repository.adicionar_historico(
            solicitacao,
            "SLA_REINICIADO",
            "SLA retomado após saída do estado de espera.",
            agora,
        )

    if dados.solucao:
        repository.adicionar_historico(
            solicitacao,
            "SOLUCAO_REGISTRADA",
            dados.solucao,
            agora,
        )

    return repository.salvar(solicitacao)
