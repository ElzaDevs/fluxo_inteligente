from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from io import StringIO
import csv

from sqlalchemy.orm import Session

from app.models.lancamento import LancamentoFinanceiro
from app.models.usuario import Usuario
from app.repositories.financeiro import FinanceiroRepository
from app.schemas.financeiro import DashboardResponse, LancamentoCreate, LancamentoUpdate


def _parse_valor(valor: str) -> Decimal:
    raw = valor.strip().replace(" ", "")
    if "," in raw and "." in raw:
        raw = raw.replace(".", "").replace(",", ".")
    elif "," in raw:
        raw = raw.replace(",", ".")
    try:
        return Decimal(raw).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Valor inválido: {valor}") from exc


class FinanceiroService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = FinanceiroRepository(db)

    def criar(self, user: Usuario, dados: LancamentoCreate) -> LancamentoFinanceiro:
        agora = datetime.now(timezone.utc)
        lancamento = LancamentoFinanceiro(
            empresa_id=user.empresa_id,
            criado_por_id=user.id,
            tipo=dados.tipo,
            descricao=dados.descricao,
            categoria=dados.categoria,
            valor=dados.valor,
            data_lancamento=dados.data_lancamento,
            status=dados.status,
            observacoes=dados.observacoes,
            created_at=agora,
            updated_at=agora,
        )
        return self.repository.salvar(lancamento)

    def atualizar(
        self,
        user: Usuario,
        lancamento_id: int,
        dados: LancamentoUpdate,
    ) -> LancamentoFinanceiro:
        lancamento = self.repository.buscar(user.empresa_id, lancamento_id)
        if not lancamento:
            raise LookupError("Lançamento não encontrado.")

        for campo, valor in dados.model_dump(exclude_unset=True).items():
            setattr(lancamento, campo, valor)

        lancamento.updated_at = datetime.now(timezone.utc)
        return self.repository.salvar(lancamento)

    def excluir(self, user: Usuario, lancamento_id: int) -> None:
        lancamento = self.repository.buscar(user.empresa_id, lancamento_id)
        if not lancamento:
            raise LookupError("Lançamento não encontrado.")
        self.repository.excluir(lancamento)

    def listar(self, user: Usuario, inicio: date | None, fim: date | None):
        return self.repository.listar(user.empresa_id, inicio, fim)

    def dashboard(self, user: Usuario, inicio: date | None = None, fim: date | None = None) -> DashboardResponse:
        hoje = date.today()
        fim = fim or hoje
        inicio = inicio or date(hoje.year, hoje.month, 1)

        lancamentos = self.repository.listar(user.empresa_id, inicio, fim)

        total_receitas = sum(
            (l.valor for l in lancamentos if l.tipo == "RECEITA" and l.status == "REALIZADO"),
            Decimal("0.00"),
        )
        total_despesas = sum(
            (l.valor for l in lancamentos if l.tipo == "DESPESA" and l.status == "REALIZADO"),
            Decimal("0.00"),
        )
        receitas_pendentes = sum(
            (l.valor for l in lancamentos if l.tipo == "RECEITA" and l.status == "PENDENTE"),
            Decimal("0.00"),
        )
        despesas_pendentes = sum(
            (l.valor for l in lancamentos if l.tipo == "DESPESA" and l.status == "PENDENTE"),
            Decimal("0.00"),
        )

        despesas_categoria: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
        for l in lancamentos:
            if l.tipo == "DESPESA" and l.status == "REALIZADO":
                despesas_categoria[l.categoria] += l.valor

        meses = {}
        cursor = date(inicio.year, inicio.month, 1)
        fim_mes = date(fim.year, fim.month, 1)
        while cursor <= fim_mes:
            meses[cursor.strftime("%Y-%m")] = {"receitas": Decimal("0.00"), "despesas": Decimal("0.00")}
            cursor = date(
                cursor.year + (1 if cursor.month == 12 else 0),
                1 if cursor.month == 12 else cursor.month + 1,
                1,
            )

        for l in lancamentos:
            chave = l.data_lancamento.strftime("%Y-%m")
            if chave not in meses:
                continue
            if l.status == "REALIZADO":
                meses[chave]["receitas" if l.tipo == "RECEITA" else "despesas"] += l.valor

        recentes = sorted(lancamentos, key=lambda x: (x.data_lancamento, x.id), reverse=True)[:10]

        from app.schemas.financeiro import CategoriaResumo, MesResumo, LancamentoResponse

        return DashboardResponse(
            periodo_inicio=inicio,
            periodo_fim=fim,
            total_receitas=total_receitas,
            total_despesas=total_despesas,
            saldo=total_receitas - total_despesas,
            receitas_pendentes=receitas_pendentes,
            despesas_pendentes=despesas_pendentes,
            quantidade_lancamentos=len(lancamentos),
            despesas_por_categoria=[
                CategoriaResumo(categoria=k, total=v)
                for k, v in sorted(despesas_categoria.items(), key=lambda item: item[1], reverse=True)[:8]
            ],
            evolucao_mensal=[
                MesResumo(mes=k, receitas=v["receitas"], despesas=v["despesas"])
                for k, v in meses.items()
            ],
            recentes=[
                LancamentoResponse(
                    id=l.id,
                    tipo=l.tipo,
                    descricao=l.descricao,
                    categoria=l.categoria,
                    valor=l.valor,
                    data_lancamento=l.data_lancamento,
                    status=l.status,
                    observacoes=l.observacoes,
                    created_at=l.created_at,
                )
                for l in recentes
            ],
        )

    def importar_csv(self, user: Usuario, conteudo: bytes) -> int:
        if len(conteudo) > 2_000_000:
            raise ValueError("Arquivo CSV maior que o limite de 2 MB.")

        texto = conteudo.decode("utf-8-sig")
        leitor = csv.DictReader(StringIO(texto))
        obrigatorios = {"tipo", "descricao", "categoria", "valor", "data_lancamento"}
        if not leitor.fieldnames or not obrigatorios.issubset(set(leitor.fieldnames)):
            raise ValueError(
                "CSV deve conter: tipo, descricao, categoria, valor, data_lancamento. "
                "status e observacoes são opcionais."
            )

        agora = datetime.now(timezone.utc)
        quantidade = 0
        for linha in leitor:
            tipo = linha["tipo"].strip().upper()
            if tipo not in {"RECEITA", "DESPESA"}:
                raise ValueError("Tipo deve ser RECEITA ou DESPESA.")

            lancamento = LancamentoFinanceiro(
                empresa_id=user.empresa_id,
                criado_por_id=user.id,
                tipo=tipo,
                descricao=linha["descricao"].strip(),
                categoria=linha["categoria"].strip(),
                valor=_parse_valor(linha["valor"]),
                data_lancamento=date.fromisoformat(linha["data_lancamento"].strip()),
                status=linha.get("status", "REALIZADO").strip().upper() or "REALIZADO",
                observacoes=(linha.get("observacoes") or "").strip() or None,
                created_at=agora,
                updated_at=agora,
            )
            if lancamento.status not in {"REALIZADO", "PENDENTE"}:
                raise ValueError("Status deve ser REALIZADO ou PENDENTE.")
            self.db.add(lancamento)
            quantidade += 1

        self.db.commit()
        return quantidade
