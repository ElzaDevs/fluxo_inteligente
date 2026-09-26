# Arquitetura

O Fluxo Inteligente usa arquitetura em camadas para separar API, aplicação, regras de negócio e persistência.

~~~text
Cliente
   |
   v
FastAPI
   |
   v
Service de Triagem
   |------> Prioridade
   |------> SLA
   |------> Encaminhamento
   |------> Status
   |
   v
Repository
   |
   v
SQLAlchemy
   |
   v
SQLite / PostgreSQL
~~~

## Responsabilidades

### API

app/main.py expõe os endpoints HTTP e controla as respostas da aplicação.

### Schemas

app/schemas/ contém os contratos de entrada e saída com Pydantic.

### Services

app/services/ orquestra o fluxo sem concentrar a regra diretamente nos endpoints.

### Rules

app/rules/ contém regras determinísticas e testáveis para prioridade, SLA, encaminhamento e status.

### Repository

app/repositories/ isola o acesso ao banco.

### Models

app/models/ representa solicitações e histórico persistidos pelo SQLAlchemy.

## Decisões

- separação de responsabilidades;
- regras de negócio testáveis isoladamente;
- persistência desacoplada;
- histórico de decisões;
- revisão humana em situações de incerteza;
- banco configurável via DATABASE_URL;
- SQLite por padrão para facilitar demonstração local;
- PostgreSQL disponível via configuração da aplicação.

## Evolução

A primeira versão não usa IA para decidir criticidade. Uma futura camada de IA pode extrair características do texto, mas a decisão deve continuar protegida pelas regras do domínio e pela revisão humana quando necessário.
