# Fluxo Inteligente

API de triagem e priorização de solicitações internas, desenvolvida como projeto de Engenharia de Software.

O sistema transforma uma solicitação desestruturada em uma decisão de atendimento rastreável, combinando regras de negócio, SLA, encaminhamento e revisão humana.

## Problema

Solicitações internas podem chegar sem prioridade clara, sem contexto suficiente ou para o setor errado.

O sistema organiza a triagem para responder:

- o que aconteceu?
- qual é o impacto?
- qual é a urgência?
- qual é a prioridade?
- qual equipe deve tratar?
- qual SLA se aplica?
- é necessária revisão humana?

## Arquitetura

~~~text
FastAPI
  |
Service de Triagem
  |---- Regra de Prioridade
  |---- Regra de SLA
  |---- Regra de Encaminhamento
  |---- Regra de Status
  |
Repository
  |
SQLAlchemy
  |
SQLite / PostgreSQL
~~~

## Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite por padrão
- PostgreSQL via DATABASE_URL
- Pytest
- HTTPX

## Funcionalidades do MVP

- registro de solicitações;
- classificação por impacto e urgência;
- matriz determinística de prioridade;
- cálculo de SLA;
- encaminhamento por categoria;
- revisão humana com justificativa;
- controle de status;
- registro de solução;
- histórico de decisões;
- testes automatizados;
- documentação técnica.

## Executando localmente

~~~bash
git clone https://github.com/ElzaDevs/fluxo_inteligente.git
cd fluxo_inteligente
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

A API ficará disponível em http://127.0.0.1:8000.

A documentação Swagger ficará disponível em http://127.0.0.1:8000/docs.

## Exemplo

~~~json
{
  "titulo": "Sistema financeiro indisponível",
  "descricao": "O sistema financeiro está indisponível para todos os funcionários.",
  "solicitante": "Elza",
  "area_solicitante": "Administrativo",
  "categoria": "TI / Sistemas",
  "impacto_informado": "critico",
  "urgencia_informada": "critica"
}
~~~

Resultado esperado no MVP:

~~~json
{
  "prioridade": "A",
  "setor_responsavel": "Tecnologia da Informação",
  "sla_horas": 2,
  "revisao_humana": false
}
~~~

## Endpoints principais

| Método | Endpoint | Objetivo |
|---|---|---|
| GET | /health | Health check |
| POST | /solicitacoes | Registrar e triar solicitação |
| GET | /solicitacoes | Listar solicitações |
| GET | /solicitacoes/{id} | Consultar solicitação e histórico |
| PATCH | /solicitacoes/{id}/revisao | Revisar decisão humana |
| PATCH | /solicitacoes/{id}/status | Controlar ciclo e registrar solução |

## Testes

~~~bash
pytest -q
~~~

A suíte cobre a matriz de prioridade, SLA, triagem e principais fluxos HTTP.

## Estrutura

~~~text
app/
├── main.py
├── database.py
├── models/
├── repositories/
├── rules/
├── schemas/
└── services/

docs/
├── arquitetura.md
├── fluxo.md
├── problema.md
├── requisitos.md
├── regras-negocio.md
├── sla.md
└── usuarios.md

tests/
├── test_api.py
├── test_prioridade.py
├── test_sla.py
└── test_triagem.py
~~~

## Limites do MVP

Este é um projeto acadêmico/portfólio. Ele não está conectado a processos corporativos reais.

Não há autenticação, autorização ou integração com sistemas internos.

Os SLAs são valores de referência definidos especificamente para demonstrar a regra de negócio do projeto.

A IA não toma decisões críticas nesta versão. Uma evolução possível é usar IA para extrair características de texto, mantendo regras determinísticas, rastreabilidade e revisão humana.

## Engenharia de Software aplicada

- Engenharia de requisitos;
- modelagem de processos;
- regras de negócio explícitas;
- arquitetura em camadas;
- separação de responsabilidades;
- API REST;
- persistência;
- testes automatizados;
- rastreabilidade;
- tratamento de incerteza;
- evolução incremental.

## Autora

**Elza Vitória Mendes Silva de Aquino**

Engenharia de Software | Python | Backend | Arquitetura de Software
