# Requisitos

## Objetivo
O sistema deve organizar o tratamento de solicitações internas recebidas pela empresa, transformando informações inicialmente desorganizadas em uma decisão estruturada de **prioridade e encaminhamento**.

A partir das informações da solicitação, o sistema deve:
1. identificar a solicitação;
2. avaliar sua urgência;
3. avaliar seu impacto;
4. determinar sua prioridade;
5. definir o setor responsável;
6. encaminhar a solicitação;
7. permitir revisão humana quando a decisão automática não apresentar confiança suficiente;
8. acompanhar a solicitação até sua solução.

O sistema não tem como objetivo substituir a decisão dos responsáveis pela empresa. A automação deve apoiar a triagem e direcionar situações que necessitem de análise humana.

---

# Requisitos Funcionais
## RF-01 — Registrar solicitação

O sistema deve permitir o registro de uma solicitação interna contendo as informações necessárias para sua triagem.

A solicitação deve possuir:

* título;
* descrição do problema ou necessidade;
* área solicitante;
* prazo, quando existente;
* informações relacionadas à urgência;
* informações relacionadas ao impacto.

Ao ser registrada, a solicitação deve receber o status **ABERTA**.

---

## RF-02 — Identificar características da solicitação

O sistema deve analisar as informações registradas para identificar características relevantes para a triagem.
A identificação deve considerar, principalmente:
* existência de prazo;
* proximidade do prazo;
* quantidade de áreas afetadas;
* abrangência do impacto;
* risco para processos da empresa;
* possível impacto financeiro;
* possibilidade de interrupção de atividade relevante.
Essas informações serão utilizadas nas etapas de avaliação e classificação.

---

## RF-03 — Avaliar urgência

O sistema deve determinar o nível de urgência da solicitação com base nas informações registradas.
A urgência deve considerar principalmente:

* se existe prazo;
* quanto tempo falta para o prazo;
* se o atraso pode gerar consequência relevante;
* se a situação exige ação imediata.

A urgência não deve ser determinada apenas pela indicação subjetiva do solicitante.

---

## RF-04 — Avaliar impacto

O sistema deve determinar o nível de impacto da solicitação.
A avaliação deve considerar:

* quantidade de pessoas ou áreas afetadas;
* abrangência dentro da empresa;
* impacto sobre processos essenciais;
* risco de prejuízo financeiro;
* risco de interrupção de operações;
* risco associado ao não atendimento.

Uma situação que afete toda a empresa deve possuir tratamento diferente de uma situação restrita a uma atividade ou área específica.

---

## RF-05 — Determinar prioridade

O sistema deve utilizar **urgência e impacto** como fatores principais para determinar a prioridade da solicitação.
A prioridade deve seguir as categorias:

| Código | Prioridade |
| ------ | ---------- |
| A      | Crítica    |
| B      | Média      |
| C      | Alta       |
| D      | Baixa      |

A definição dos critérios utilizados para cada categoria deve estar documentada em `regras-negocio.md`.
A prioridade não deve ser definida arbitrariamente pelo sistema.

---

## RF-06 — Verificar confiança da classificação

Antes de aceitar uma classificação automática, o sistema deve verificar se existem informações suficientes e consistentes para sustentar a decisão.
Quando os dados forem insuficientes, conflitantes ou não atenderem ao nível mínimo de confiança definido pelas regras do sistema, a solicitação não deve ser classificada automaticamente.
Nesse caso, deve ser encaminhada para **REVISÃO HUMANA**.

---

## RF-07 — Realizar revisão humana

O sistema deve permitir que um responsável revise uma solicitação encaminhada para análise humana.
Durante a revisão, o responsável poderá:

* confirmar a prioridade;
* alterar a prioridade;
* corrigir a avaliação de impacto;
* corrigir a avaliação de urgência;
* corrigir o setor responsável;
* justificar a alteração realizada.

A decisão da revisão deve ficar registrada no histórico da solicitação.

---

## RF-08 — Determinar setor responsável

Após a triagem, o sistema deve determinar o setor responsável pelo atendimento da solicitação.
O encaminhamento deve considerar o assunto e as características identificadas na solicitação,
Os setores inicialmente considerados pelo projeto são:

* **Gestão da Economia**
* **Analistas de Suporte**
* **Setor Financeiro**
* **Tecnologia da Informação**
O conjunto de setores poderá ser ampliado posteriormente.

---

## RF-09 — Encaminhar solicitação
Após a classificação e definição do setor responsável, o sistema deve encaminhar a solicitação para o setor correspondente.

O encaminhamento deve registrar:
* setor responsável;
* data e hora do encaminhamento;
* prioridade definida;
* responsável pela decisão, quando houver revisão humana.

---

## RF-10 — Controlar ciclo da solicitação
A solicitação deve seguir um ciclo de atendimento controlado pelo sistema:

```text
ABERTA
   ↓
EM ANÁLISE
   ↓
EM PROCESSO
   ↓
SOLUÇÃO
```

O sistema deve registrar o status atual e as alterações realizadas durante o ciclo.

---
## RF-11 — Registrar histórico da decisão

O sistema deve manter o histórico das decisões relacionadas à triagem.
Devem ser registrados, quando aplicável:

* classificação inicial;
* prioridade inicial;
* avaliação de impacto;
* avaliação de urgência;
* setor inicialmente definido;
* revisão humana;
* alteração de prioridade;
* alteração de setor;
* responsável pela alteração;
* data e hora da alteração;
* justificativa da alteração.
O objetivo é permitir compreender **como e por que uma solicitação recebeu determinada classificação e encaminhamento**.

---
## RF-12 — Acompanhar solicitação

O sistema deve permitir consultar uma solicitação e visualizar:

* informações registradas;
* prioridade atual;
* impacto;
* urgência;
* setor responsável;
* status atual;
* histórico de decisões;
* solução registrada, quando concluída.

---
## RF-13 — Registrar solução

Quando o atendimento for concluído, o sistema deve permitir registrar a solução aplicada.

Após o registro da solução, a solicitação poderá assumir o status **SOLUÇÃO**.

A solução deve permanecer associada ao histórico da solicitação.

---
# 3. Regras essenciais do sistema

O funcionamento dos requisitos deve obedecer às seguintes premissas:

### RQ-01 — Impacto e urgência são distintos

Impacto representa **o tamanho da consequência para a empresa**.

Urgência representa **a necessidade temporal de atendimento**.

Os dois fatores devem ser avaliados separadamente antes da determinação da prioridade.

### RQ-02 — Alta urgência não significa automaticamente impacto crítico

Uma solicitação pode exigir atendimento rápido sem afetar significativamente a empresa.

Portanto, urgência e impacto não devem ser tratados como sinônimos.

### RQ-03 — Impacto crítico exige atenção diferenciada

Situações que possam afetar a empresa de forma ampla, interromper processos relevantes ou representar risco crítico devem ser identificadas como situações de alta relevância para a triagem.

### RQ-04 — Decisão automática possui limite

O sistema não deve forçar uma classificação quando as informações disponíveis não forem suficientes para sustentar a decisão.

Nessas situações, a decisão deve passar por revisão humana.

### RQ-05 — Toda alteração relevante deve ser rastreável

Quando uma pessoa alterar uma decisão realizada durante a triagem, o sistema deve registrar o que foi alterado, por quem, quando e, quando aplicável, o motivo.

---
# 4. Fora do escopo da primeira versão

A primeira versão não terá como objetivo:

* substituir gestores ou analistas na tomada de decisões;
* executar ações diretamente nos processos dos setores;
* realizar movimentações financeiras;
* acessar documentos ou sistemas internos reais de uma empresa;
* tomar decisões críticas sem possibilidade de revisão;
* integrar automaticamente todos os sistemas corporativos;
* utilizar inteligência artificial sem critérios definidos para sua aplicação.

A inteligência artificial poderá ser incorporada posteriormente como mecanismo de apoio à identificação e classificação, respeitando as regras de confiança e revisão humana definidas pelo projeto.

---

# 5. Resultado esperado

Ao final do fluxo, uma solicitação que inicialmente chega de forma desorganizada deve possuir uma estrutura clara:

```text
SOLICITAÇÃO
    ↓
IMPACTO + URGÊNCIA
    ↓
PRIORIDADE
    ↓
SETOR RESPONSÁVEL
    ↓
ACOMPANHAMENTO
    ↓
SOLUÇÃO
```

Quando não houver informação suficiente para uma decisão confiável:

```text
SOLICITAÇÃO
    ↓
IMPACTO + URGÊNCIA
    ↓
INCERTEZA
    ↓
REVISÃO HUMANA
    ↓
PRIORIDADE + SETOR
    ↓
ACOMPANHAMENTO
    ↓
SOLUÇÃO
```
O resultado esperado do sistema é reduzir **encaminhamentos incorretos, perda de prazos, dificuldade de identificar situações críticas e decisões inconsistentes** durante a triagem das solicitações internas.
