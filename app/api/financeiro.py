from datetime import date, datetime
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user, require_csrf
from app.models.usuario import Usuario
from app.schemas.financeiro import (
    DashboardResponse,
    LancamentoCreate,
    LancamentoResponse,
    LancamentoUpdate,
)
from app.services.financeiro import FinanceiroService

router = APIRouter(prefix="/financeiro", tags=["Financeiro"])


def _response(lancamento):
    return LancamentoResponse(
        id=lancamento.id,
        tipo=lancamento.tipo,
        descricao=lancamento.descricao,
        categoria=lancamento.categoria,
        valor=lancamento.valor,
        data_lancamento=lancamento.data_lancamento,
        status=lancamento.status,
        observacoes=lancamento.observacoes,
        created_at=lancamento.created_at,
    )


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(
    inicio: date | None = Query(default=None),
    fim: date | None = Query(default=None),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if inicio and fim and inicio > fim:
        raise HTTPException(status_code=422, detail="Período inválido.")
    return FinanceiroService(db).dashboard(user, inicio, fim)


@router.get("/lancamentos", response_model=list[LancamentoResponse])
def listar_lancamentos(
    inicio: date | None = Query(default=None),
    fim: date | None = Query(default=None),
    user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return [_response(x) for x in FinanceiroService(db).listar(user, inicio, fim)]


@router.post("/lancamentos", response_model=LancamentoResponse, status_code=201)
def criar_lancamento(
    dados: LancamentoCreate,
    user: Usuario = Depends(require_csrf),
    db: Session = Depends(get_db),
):
    return _response(FinanceiroService(db).criar(user, dados))


@router.put("/lancamentos/{lancamento_id}", response_model=LancamentoResponse)
def atualizar_lancamento(
    lancamento_id: int,
    dados: LancamentoUpdate,
    user: Usuario = Depends(require_csrf),
    db: Session = Depends(get_db),
):
    try:
        item = FinanceiroService(db).atualizar(user, lancamento_id, dados)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return _response(item)


@router.delete("/lancamentos/{lancamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_lancamento(
    lancamento_id: int,
    user: Usuario = Depends(require_csrf),
    db: Session = Depends(get_db),
):
    try:
        FinanceiroService(db).excluir(user, lancamento_id)
    except LookupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/importar-csv")
async def importar_csv(
    arquivo: UploadFile = File(...),
    user: Usuario = Depends(require_csrf),
    db: Session = Depends(get_db),
):
    if not arquivo.filename or not arquivo.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=422, detail="Envie um arquivo CSV.")

    try:
        conteudo = await arquivo.read()
        quantidade = FinanceiroService(db).importar_csv(user, conteudo)
    except (ValueError, UnicodeDecodeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {"importados": quantidade}
