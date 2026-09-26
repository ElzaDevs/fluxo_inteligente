# Fluxo Inteligente

Sistema web multiempresa para gestão financeira e triagem operacional.

O objetivo é simular um cenário empresarial real: uma organização cadastra sua conta, acessa um ambiente protegido, registra receitas e despesas, importa dados, acompanha indicadores financeiros e também organiza solicitações internas com prioridade, SLA e rastreabilidade.

Este é um projeto de portfólio executável. Não é apresentado como sistema já contratado ou usado em produção por uma empresa.

## Fluxo principal

~~~text
Cadastro da empresa
       |
       v
Login
       |
       v
Dashboard
  |            |
  v            v
Financeiro   Triagem
  |            |
  v            v
Receitas     Prioridade
Despesas     SLA
Importação   Encaminhamento
  |
  v
Indicadores e gráficos reais
~~~

## Funcionalidades

### Conta empresarial

- cadastro da empresa;
- criação do primeiro administrador;
- login;
- logout;
- sessão com expiração;
- senha armazenada com hash Argon2;
- proteção CSRF;
- isolamento por empresa.

### Financeiro

- cadastro de receita;
- cadastro de despesa;
- edição;
- exclusão;
- status realizado ou pendente;
- filtro por período;
- saldo calculado;
- fluxo mensal;
- despesas por categoria;
- lançamentos recentes;
- importação CSV.

### Triagem

- impacto;
- urgência;
- matriz de prioridade;
- SLA de resposta;
- SLA de resolução;
- calendário 24x7 e horário comercial;
- pausa do SLA por dependência;
- encaminhamento;
- revisão humana;
- histórico.

## Arquitetura

~~~text
Browser
   |
Templates + JavaScript + CSS
   |
FastAPI
   |
   +---- Auth
   |
   +---- Financeiro Service
   |
   +---- Triagem Service
   |
Rules + Repositories
   |
SQLAlchemy
   |
SQLite / PostgreSQL
~~~

A aplicação separa apresentação, API, serviços, regras e persistência para manter o código evolutivo e testável.

## Stack

- Python 3.12
- FastAPI
- Jinja2
- Pydantic
- SQLAlchemy
- PostgreSQL + psycopg
- SQLite
- pwdlib + Argon2
- Pytest
- HTTPX
- Docker
- GitHub Actions

## Como executar

~~~bash
python -m venv .venv
~~~

Windows:

~~~powershell
.venv\Scripts\activate
~~~

Linux/macOS:

~~~bash
source .venv/bin/activate
~~~

Instale:

~~~bash
pip install -r requirements.txt
~~~

Execute:

~~~bash
uvicorn app.main:app --reload
~~~

Acesse:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/cadastro
- http://127.0.0.1:8000/login
- http://127.0.0.1:8000/dashboard
- http://127.0.0.1:8000/docs

## Docker

~~~bash
docker compose up --build
~~~

O compose sobe a aplicação e PostgreSQL para demonstração local.

## Banco

Sem configuração adicional, a aplicação usa:

~~~text
sqlite:///./fluxo_inteligente.db
~~~

Para PostgreSQL:

~~~text
postgresql+psycopg://usuario:senha@host:5432/banco
~~~

## CSV

O arquivo docs/exemplo-lancamentos.csv pode ser usado como modelo de carga.

Colunas:

~~~text
tipo,descricao,categoria,valor,data_lancamento,status,observacoes
~~~

O importador aceita tanto valores com ponto decimal quanto valores no padrão brasileiro com vírgula.

## API

Autenticação:

~~~text
POST /auth/register
POST /auth/login
POST /auth/logout
GET  /auth/me
GET  /auth/csrf
~~~

Financeiro:

~~~text
GET    /financeiro/dashboard
GET    /financeiro/lancamentos
POST   /financeiro/lancamentos
PUT    /financeiro/lancamentos/{id}
DELETE /financeiro/lancamentos/{id}
POST   /financeiro/importar-csv
~~~

Triagem:

~~~text
POST  /solicitacoes
GET   /solicitacoes
GET   /solicitacoes/{id}
PATCH /solicitacoes/{id}/revisao
PATCH /solicitacoes/{id}/status
~~~

## Testes

~~~bash
pytest -q
~~~

A suíte cobre autenticação, CRUD financeiro, importação, dashboard, triagem, matriz de prioridade, SLA e transições de status.

## Limites para produção

Antes de armazenar dados empresariais reais, ainda seriam necessários mecanismos como HTTPS, rate limiting, MFA, recuperação de senha, RBAC detalhado, gestão de segredos, observabilidade, backups, migrações de banco, políticas de retenção e revisão de segurança.

Os SLAs utilizados são valores de referência da simulação. Em uma implantação real, seriam parametrizados conforme o serviço e o contrato.

## Competências demonstradas

- Engenharia de Software
- Arquitetura em camadas
- Backend Python/FastAPI
- APIs REST
- Autenticação e segurança
- Modelagem de dados
- PostgreSQL/SQLAlchemy
- Dashboard orientado a dados
- Regras de negócio
- SLA/ITSM
- Testes automatizados
- CI
- Importação de dados
- Rastreabilidade

## Autora

Elza Vitória Mendes Silva de Aquino

Engenharia de Software · Python · Backend · Arquitetura de Software
