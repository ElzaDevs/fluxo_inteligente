from uuid import uuid4

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


def registrar(email=None):
    email = email or f"teste-{uuid4().hex[:10]}@empresa.com"
    response = client.post(
        "/auth/register",
        json={
            "empresa": "Empresa Teste",
            "nome": "Usuário Teste",
            "email": email,
            "senha": "SenhaForte123!",
        },
    )
    assert response.status_code == 201
    return response


def csrf():
    response = client.get("/auth/csrf")
    assert response.status_code == 200
    return response.json()["csrf_token"]


def lancamento(**kwargs):
    data = {
        "tipo": "RECEITA",
        "descricao": "Venda de serviço",
        "categoria": "Vendas",
        "valor": 1500.00,
        "data_lancamento": "2026-09-15",
        "status": "REALIZADO",
        "observacoes": "Receita de teste",
    }
    data.update(kwargs)
    return data


def test_cadastro_login_logout():
    email = f"{uuid4().hex[:10]}@empresa.com"
    response = registrar(email)
    assert response.json()["empresa"]["nome"] == "Empresa Teste"

    response = client.get("/auth/me")
    assert response.status_code == 200
    assert response.json()["usuario"]["email"] == email

    token = csrf()
    response = client.post("/auth/logout", headers={"X-CSRF-Token": token})
    assert response.status_code == 204

    response = client.get("/auth/me")
    assert response.status_code == 401

    response = client.post(
        "/auth/login",
        json={"email": email, "senha": "SenhaForte123!"},
    )
    assert response.status_code == 200


def test_crud_financeiro_e_dashboard():
    registrar()

    token = csrf()
    response = client.post(
        "/financeiro/lancamentos",
        json=lancamento(),
        headers={"X-CSRF-Token": token},
    )
    assert response.status_code == 201
    lancamento_id = response.json()["id"]

    response = client.post(
        "/financeiro/lancamentos",
        json=lancamento(
            tipo="DESPESA",
            descricao="Folha",
            categoria="Pessoal",
            valor=400.00,
        ),
        headers={"X-CSRF-Token": csrf()},
    )
    assert response.status_code == 201

    response = client.get("/financeiro/dashboard?inicio=2026-09-01&fim=2026-09-30")
    assert response.status_code == 200
    body = response.json()
    assert body["total_receitas"] == 1500.0
    assert body["total_despesas"] == 400.0
    assert body["saldo"] == 1100.0
    assert body["quantidade_lancamentos"] == 2

    response = client.put(
        f"/financeiro/lancamentos/{lancamento_id}",
        json={"valor": 2000.00},
        headers={"X-CSRF-Token": csrf()},
    )
    assert response.status_code == 200
    assert response.json()["valor"] == 2000.0

    response = client.delete(
        f"/financeiro/lancamentos/{lancamento_id}",
        headers={"X-CSRF-Token": csrf()},
    )
    assert response.status_code == 204


def test_importacao_csv():
    registrar()

    csv_content = (
        "tipo,descricao,categoria,valor,data_lancamento,status,observacoes\n"
        "RECEITA,Contrato A,Vendas,\"1.250,50\",2026-09-10,REALIZADO,CSV\n"
        "DESPESA,Internet,Infraestrutura,120.00,2026-09-11,REALIZADO,CSV\n"
    )

    response = client.post(
        "/financeiro/importar-csv",
        files={"arquivo": ("dados.csv", csv_content, "text/csv")},
        headers={"X-CSRF-Token": csrf()},
    )

    assert response.status_code == 200
    assert response.json()["importados"] == 2


def test_solicitacoes_exigem_autenticacao():
    client.post("/auth/logout", headers={"X-CSRF-Token": csrf()})
    response = client.get("/solicitacoes")
    assert response.status_code == 401


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
