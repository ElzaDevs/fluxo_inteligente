# Arquitetura

O Fluxo Inteligente é uma aplicação web multiempresa com dois domínios principais:

1. Gestão financeira.
2. Triagem operacional de solicitações.

A aplicação utiliza separação de responsabilidades entre apresentação, API, serviços, regras de negócio, persistência e autenticação.

~~~text
                          BROWSER
                             |
                    HTML + CSS + JavaScript
                             |
                        FASTAPI APP
          _________________/ | \________________
         /                  |                   \
        v                   v                    v
      AUTH              FINANCEIRO            TRIAGEM
        |                   |                    |
        v                   v                    v
     Sessões            Dashboard             Prioridade
     Usuários           CRUD                  SLA
     Empresas           CSV                   Encaminhamento
                         |                    Revisão
                         |                    Histórico
                         \___________  __________/
                                     \/
                                REPOSITORIES
                                     |
                                  SQLALCHEMY
                                     |
                          SQLite / PostgreSQL
~~~

## Domínio de autenticação

Empresa é a unidade de isolamento.

~~~text
Empresa
  |
  +-- Usuários
  |
  +-- Sessões
  |
  +-- Lançamentos financeiros
  |
  +-- Solicitações
~~~

O primeiro usuário criado no cadastro recebe perfil ADMIN.

As senhas são armazenadas somente como hash.

As sessões utilizam tokens aleatórios, armazenados como hash no banco, com expiração e revogação.

Operações de escrita da interface utilizam um token CSRF separado do cookie de sessão.

## Domínio financeiro

Um lançamento possui:

- tipo;
- descrição;
- categoria;
- valor;
- data;
- status;
- observações;
- empresa;
- usuário que criou o registro.

O dashboard consulta os dados persistidos e calcula os indicadores do período.

### Indicadores

~~~text
Lançamentos
   |
   +-- Receitas realizadas
   +-- Despesas realizadas
   +-- Saldo
   +-- Pendências
   +-- Evolução mensal
   +-- Despesas por categoria
   +-- Últimos lançamentos
~~~

Os gráficos são alimentados pela resposta real da API.

## Domínio de triagem

Solicitações são vinculadas à empresa autenticada.

O fluxo é:

~~~text
Solicitação
    |
    v
Impacto + Urgência
    |
    v
Matriz de prioridade
    |
    v
SLA
    |
    v
Encaminhamento
    |
    +--> Revisão humana quando necessário
    |
    v
Histórico + status
~~~

## SLA

A política do projeto diferencia:

- tempo de resposta;
- tempo de resolução;
- calendário 24x7;
- horário comercial;
- pausa por dependências externas;
- retomada;
- cumprimento ou violação.

Os valores são de referência da simulação e não representam contrato de uma organização específica.

## Persistência

SQLite é usado como padrão para facilitar execução local.

PostgreSQL pode ser utilizado configurando DATABASE_URL.

O acesso aos dados passa pelos repositories para evitar que os endpoints conheçam detalhes de persistência.

## API

Os routers são separados por responsabilidade:

~~~text
app/api/
├── auth.py
├── financeiro.py
├── solicitacoes.py
└── web.py
~~~

Isso reduz o acoplamento e facilita a evolução do sistema.

## Qualidade

O projeto inclui:

- testes unitários das regras;
- testes da triagem;
- testes HTTP;
- GitHub Actions para executar a suíte;
- Docker;
- documentação técnica;
- .env.example;
- isolamento multiempresa.

## Próximas evoluções

Para uma implantação corporativa seriam apropriados:

- Alembic para migrações;
- RBAC detalhado;
- rate limiting;
- MFA;
- recuperação de senha;
- observabilidade;
- auditoria de segurança;
- backups;
- integração com ERP/bancos;
- infraestrutura de produção.

A arquitetura atual foi organizada para permitir essas evoluções sem concentrar as regras de domínio na camada HTTP.
