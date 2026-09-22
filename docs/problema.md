# Problema

## Contexto

Uma organização pode receber um grande volume de solicitações internas
relacionadas a diferentes áreas, processos e sistemas.
Essas solicitações podem apresentar diferentes níveis de urgência,
impacto e risco, além de serem encaminhadas inicialmente para áreas
que não possuem responsabilidade ou capacidade para tratá-las.
Quando não existe um processo padronizado para analisar e priorizar
essas solicitações, situações críticas podem receber o mesmo tratamento
que demandas de menor impacto.
## Impactos

A ausência de uma priorização e de um encaminhamento padronizados pode
contribuir para:

- atrasos no atendimento;
- encaminhamento incorreto de solicitações;
- perda de prazos;
- descumprimento de SLA;
- dificuldade para identificar situações críticas;
- sobrecarga de determinadas equipes;
- decisões inconsistentes entre diferentes analistas;
- dificuldade para acompanhar o volume e o status das solicitações.

## Objetivo

Desenvolver um sistema capaz de receber solicitações internas,
avaliar suas características com base em regras de negócio,
determinar sua prioridade, definir o SLA aplicável e recomendar
a equipe responsável pelo atendimento.
Quando as informações disponíveis forem insuficientes ou houver
baixa confiança na classificação, o sistema deverá encaminhar
a solicitação para revisão humana.

## O que o sistema recebe?

Inicialmente, o sistema deverá receber:

- Descrição da solicitação;
- Categoria;
- Solicitante;
- Impacto informado ou identificado;
- Urgência informada ou identificada;
- Evidências ou informações complementares, quando aplicável.

## Exemplo

### Solicitação

**Descrição:**

> "O sistema financeiro está indisponível para todos os funcionários."

**Categoria:**

TI / Sistemas

**Impacto:**

Organização inteira

**Urgência:**

Crítica

### Resultado esperado

O sistema deverá avaliar as informações da solicitação e determinar:

- Prioridade: Crítica.
- Equipe responsável: TI / Suporte de Sistemas.
- SLA aplicável: definido conforme as regras de negócio.
- Status inicial: Aberta.
- Necessidade de revisão humana: conforme os critérios de confiança.
  e consistência definidos pelo sistema.

## O que o sistema precisa decidir?

A partir das informações recebidas e das regras de negócio, o sistema
deverá determinar ou recomendar:

- Prioridade da solicitação;
- Equipe responsável;
- SLA aplicável;
- Status da solicitação;
- Necessidade de revisão humana.

## Resultado esperado

O sistema deverá transformar uma solicitação inicialmente desestruturada
em uma ocorrência classificada, priorizada e encaminhada de forma
rastreável.
O processo deverá permitir identificar:

1. O que aconteceu?
2. Qual é o impacto?
3. Qual é a urgência?
4. Qual é a prioridade?
5. Quem deve tratar?
6. Em quanto tempo deve ser tratado?
7. Se é necessária intervenção humana?
8. Qual foi o resultado do atendimento?