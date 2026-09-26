from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionTeste = sessionmaker(bind=engine_teste, autoflush=False, autocommit=False)
Base.metadata.create_all(bind=engine_teste)


def override_get_db():
    db = SessionTeste()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def payload(**kwargs):
    data = {
        "titulo": "Sistema financeiro indisponível",
        "descricao": "O sistema financeiro está indisponível para todos os funcionários.",
        "solicitante": "Elza",
        "area_solicitante": "Administrativo",
        "categoria": "TI / Sistemas",
        "impacto_informado": "critico",
        "urgencia_informada": "critica",
    }
    data.update(kwargs)
    return data


def test_criar_solicitacao_completa():
    response = client.post("/solicitacoes", json=payload())

    assert response.status_code == 201
    body = response.json()

    assert body["prioridade"] == "A"
    assert body["setor_responsavel"] == "Tecnologia da Informação"
    assert body["sla_resposta_minutos"] == 15
    assert body["sla_resolucao_minutos"] == 240
    assert body["sla_status"] == "RUNNING"
    assert body["revisao_humana"] is False


def test_solicitacao_incompleta_vai_para_revisao():
    response = client.post(
        "/solicitacoes",
        json=payload(impacto_informado=None),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["revisao_humana"] is True
    assert body["prioridade"] is None
    assert body["sla_status"] == "PENDING_REVIEW"


def test_fluxo_de_status_e_solucao():
    response = client.post("/solicitacoes", json=payload())
    solicitacao_id = response.json()["id"]

    assert client.patch(
        f"/solicitacoes/{solicitacao_id}/status",
        json={"status": "EM_ANALISE"},
    ).status_code == 200

    assert client.patch(
        f"/solicitacoes/{solicitacao_id}/status",
        json={"status": "EM_PROCESSO"},
    ).status_code == 200

    response = client.patch(
        f"/solicitacoes/{solicitacao_id}/status",
        json={
            "status": "SOLUCAO",
            "solucao": "Serviço restaurado e operação normalizada.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "SOLUCAO"
    assert body["sla_status"] == "MET"


def test_sla_pode_ser_pausado_e_retomado():
    response = client.post("/solicitacoes", json=payload())
    solicitacao_id = response.json()["id"]

    client.patch(
        f"/solicitacoes/{solicitacao_id}/status",
        json={"status": "EM_ANALISE"},
    )
    client.patch(
        f"/solicitacoes/{solicitacao_id}/status",
        json={"status": "EM_PROCESSO"},
    )

    response = client.patch(
        f"/solicitacoes/{solicitacao_id}/status",
        json={"status": "AGUARDANDO_SOLICITANTE"},
    )
    assert response.status_code == 200
    assert response.json()["sla_status"] == "PAUSED"
    assert response.json()["sla_paused_at"] is not None

    response = client.patch(
        f"/solicitacoes/{solicitacao_id}/status",
        json={"status": "EM_PROCESSO"},
    )
    assert response.status_code == 200
    assert response.json()["sla_status"] == "RUNNING"
    assert response.json()["sla_paused_at"] is None


def test_transicao_invalida():
    response = client.post("/solicitacoes", json=payload())
    solicitacao_id = response.json()["id"]

    response = client.patch(
        f"/solicitacoes/{solicitacao_id}/status",
        json={"status": "SOLUCAO", "solucao": "Tentativa inválida."},
    )

    assert response.status_code == 409


def test_buscar_solicitacao_inexistente():
    response = client.get("/solicitacoes/99999")
    assert response.status_code == 404
