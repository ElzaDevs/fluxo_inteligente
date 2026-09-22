# Fluxo da solicitação

O fluxo representa o caminho que uma solicitação percorre desde o momento em que é registrada até sua solução.

O ponto principal do sistema é a **triagem**. É nessa etapa que uma solicitação inicialmente desorganizada passa a ter uma prioridade e um encaminhamento definidos.

## 1. Abertura

O solicitante registra o problema ou necessidade.

```text
ABERTA
```

Nesse momento, a solicitação ainda não possui uma decisão definitiva de prioridade ou encaminhamento.

---

## 2. Identificação

O sistema organiza as informações recebidas para entender o contexto da solicitação.

São observados elementos como:

* o que aconteceu;
* quem foi afetado;
* qual área está envolvida;
* existe prazo;
* qual consequência pode ocorrer se nada for feito.

---

## 3. Avaliação

A solicitação passa por duas análises diferentes.

### Impacto

Procura entender o tamanho da consequência para a empresa.

Exemplo:

> Um problema restrito a uma atividade de uma área possui uma abrangência diferente de um problema que impede várias áreas de trabalharem.

### Urgência

Procura entender quanto tempo existe para agir.

Exemplo:

> Uma solicitação com prazo para o mesmo dia pode exigir uma resposta mais rápida do que outra que pode ser tratada posteriormente.

Impacto e urgência são analisados separadamente.

---

## 4. Classificação

Depois da avaliação, o sistema determina uma prioridade:

```text
A — Crítica
B — Média
C — Alta
D — Baixa
```

A classificação deve seguir as regras definidas em `regras-negocio.md`.

---

## 5. Verificação

Antes de seguir automaticamente, o sistema verifica se existem informações suficientes para sustentar a classificação.

### Quando a informação é suficiente

A solicitação segue para o encaminhamento.

```text
CLASSIFICAÇÃO
      ↓
ENCAMINHAMENTO
```

### Quando a informação não é suficiente

A solicitação vai para revisão humana.

```text
CLASSIFICAÇÃO
      ↓
REVISÃO HUMANA
      ↓
NOVA DECISÃO
```

Isso evita que o sistema trate uma decisão incerta como se fosse uma decisão segura.

---

## 6. Encaminhamento

Com a prioridade definida, o sistema determina o setor responsável.

```text
PRIORIDADE
    +
CARACTERÍSTICAS DA SOLICITAÇÃO
    ↓
SETOR RESPONSÁVEL
```

O encaminhamento deve ficar registrado para que seja possível entender posteriormente como a solicitação chegou àquela equipe.

---

## 7. Atendimento

Depois do encaminhamento, a solicitação passa pelos estados:

```text
ABERTA
  ↓
EM ANÁLISE
  ↓
EM PROCESSO
  ↓
SOLUÇÃO
```

### EM ANÁLISE

A equipe recebeu a solicitação e está entendendo o problema.

### EM PROCESSO

A equipe já iniciou as ações necessárias para resolver a situação.

### SOLUÇÃO

O atendimento foi concluído e a solução foi registrada.

---

## 8. Histórico

Durante todo o processo, as principais decisões devem permanecer registradas.

Assim, caso uma prioridade ou setor seja alterado, será possível identificar:

* o que foi alterado;
* quem realizou a alteração;
* quando ocorreu;
* qual era a decisão anterior;
* qual foi a nova decisão;
* motivo da alteração, quando informado.

---

## Visão completa

```text
                    ┌──────────────────┐
                    │   SOLICITAÇÃO    │
                    └────────┬─────────┘
                             ↓
                    ┌──────────────────┐
                    │   IDENTIFICAR    │
                    └────────┬─────────┘
                             ↓
                ┌────────────┴────────────┐
                ↓                         ↓
        ┌──────────────┐          ┌──────────────┐
        │   IMPACTO    │          │   URGÊNCIA   │
        └──────┬───────┘          └──────┬───────┘
               └────────────┬────────────┘
                            ↓
                    ┌──────────────────┐
                    │   CLASSIFICAR    │
                    └────────┬─────────┘
                             ↓
                  ┌─────────────────────┐
                  │ Informação suficiente? │
                  └──────────┬──────────┘
                       SIM    │    NÃO
                        ↓     │     ↓
                 ┌──────────┐ │ ┌──────────────┐
                 │ENCAMINHAR│ │ │ REVISÃO      │
                 └────┬─────┘ │ │ HUMANA       │
                      │       │ └──────┬───────┘
                      │       │        ↓
                      │       │  NOVA DECISÃO
                      │       │        │
                      └───────┴────────┘
                              ↓
                       EM ANÁLISE
                              ↓
                       EM PROCESSO
                              ↓
                          SOLUÇÃO
```
