# Regras de negócio
As regras de negócio definem como o sistema deve interpretar uma solicitação e tomar decisões durante a triagem.
O objetivo não é apenas atribuir uma prioridade. É fazer com que a decisão tenha uma justificativa clara e possa ser revisada quando necessário.

---

## 1. Impacto e urgência são avaliados separadamente
O sistema deve analisar dois aspectos diferentes:

### Impacto

Indica **o tamanho da consequência que a situação pode causar**.

O impacto pode estar relacionado a:

* uma atividade específica;
* uma área;
* várias áreas;
* grande parte da empresa;
* a empresa como um todo;
* risco financeiro relevante;
* interrupção de processos importantes.

### Urgência

Indica **quanto tempo existe para agir antes que a situação gere uma consequência maior**.
A urgência deve considerar:

* existência de prazo;
* proximidade do prazo;
* consequência do atraso;
* necessidade de intervenção imediata.

Uma solicitação pode ter impacto alto e não ser urgente naquele momento
Da mesma forma, pode ser urgente sem representar um grande impacto para a empresa.
Por isso, os dois fatores não devem ser tratados como a mesma coisa.

---

# 2. Classificação do impacto
Para facilitar a análise, o impacto será dividido em quatro níveis.

## Impacto baixo

A situação está limitada a uma atividade ou contexto específico e não apresenta consequência relevante para outras áreas.
Exemplo:
> Uma dificuldade que afeta apenas uma tarefa interna e possui alternativa de execução.

---

## Impacto médio
A situação afeta uma área ou processo importante, mas existe possibilidade de continuar trabalhando por outro meio.
Exemplo:

> Um recurso utilizado por uma equipe deixa de funcionar, mas a atividade pode continuar temporariamente por outro procedimento.

---

## Impacto alto
A situação afeta mais de uma área ou um processo relevante e pode gerar prejuízo, atraso ou interrupção significativa caso não seja tratada.
Exemplo:

> Um problema em um processo compartilhado começa a impedir o trabalho de várias equipes.

---

## Impacto crítico

A situação pode afetar a empresa de forma ampla, interromper um processo essencial ou representar risco crítico para a operação.
Exemplo:

> Uma falha que impede várias áreas de executar uma atividade essencial da empresa.
O impacto crítico deve receber atenção diferenciada durante a triagem.

---

# Classificação da urgência
A urgência também será analisada separadamente.

## Urgência baixa
Existe tempo suficiente para tratar a solicitação sem consequência relevante por esperar.

---

## Urgência média
Existe um prazo ou uma necessidade de atendimento, mas ainda há margem para planejamento.

---

## Urgência alta
O prazo está próximo ou o atraso pode gerar uma consequência relevante.

---

## Urgência crítica
A situação exige intervenção imediata ou o atraso pode causar uma consequência grave.

---

# 4. Definição da prioridade
A prioridade será determinada considerando **impacto + urgência**.

A prioridade não deve ser definida apenas por um dos dois fatores.
As categorias utilizadas pelo sistema são:

| Prioridade      | Significado                                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------------------------- |
| **A — Crítica** | Situação que exige atenção imediata devido à combinação de alto impacto e/ou consequência grave associada ao tempo. |
| **B — Média**   | Situação relevante que precisa ser tratada, mas não apresenta características de uma situação crítica.              |
| **C — Alta**    | Situação que possui necessidade significativa de atendimento e não deve ser deixada sem acompanhamento.             |
| **D — Baixa**   | Situação que pode ser planejada e tratada posteriormente sem consequência relevante no curto prazo.                 |

> **Observação:** a matriz definitiva entre impacto e urgência será definida antes da implementação, evitando que essas categorias sejam interpretadas de maneira diferente no código.
---

# 5. Situações que exigem atenção imediata

Independentemente de outros fatores, uma solicitação deve ser tratada como situação de atenção crítica quando apresentar evidências de:
* risco de interrupção de um processo essencial;
* impacto potencial para grande parte da empresa;
* risco financeiro relevante e imediato;
* prazo imediato associado a uma consequência grave;
* combinação de alto impacto e alta urgência.
Essas situações não devem ficar aguardando uma classificação automática sem análise adequada.

---

# 6. Quando a classificação automática pode acontecer

A classificação automática só deve ocorrer quando o sistema tiver informações suficientes para sustentar a decisão.
Para isso, a solicitação precisa apresentar informações claras sobre os fatores utilizados na triagem.

Por exemplo:

* impacto identificado;
* urgência identificada;
* consequência do atraso conhecida;
* abrangência compreendida;
* setor potencialmente responsável identificável.

---

# 7. Quando a solicitação deve ir para revisão humana

A solicitação deve ser encaminhada para revisão humana quando:

* faltarem informações importantes;
* houver informações contraditórias;
* o impacto não puder ser determinado com segurança;
* a urgência não puder ser determinada com segurança;
* houver dúvida entre classificações relevantes;
* a situação apresentar características críticas que não possam ser avaliadas adequadamente de forma automática.
A revisão humana existe para lidar com situações em que o contexto não pode ser reduzido com segurança às informações disponíveis.

---

# 8. Revisão pode alterar a decisão
O responsável pela revisão poderá alterar:

* impacto;
* urgência;
* prioridade;
* setor responsável.

A alteração deve ser registrada no histórico.
O sistema não deve apagar a decisão anterior. Deve manter o registro da mudança.

---

# 9. Encaminhamento

A prioridade e as características da solicitação devem ajudar a determinar para qual setor ela será encaminhada.
O setor responsável não deve ser escolhido somente pela prioridade.
A decisão deve considerar principalmente **o assunto e a natureza do problema**.

Exemplos:
* questões relacionadas a processos financeiros → **Setor Financeiro**;
* questões relacionadas a sistemas e tecnologia → **Tecnologia da Informação**;
* questões relacionadas a suporte → **Analistas de Suporte**;
* questões relacionadas à gestão econômica → **Gestão da Economia**.
Quando o assunto não permitir determinar o setor com segurança, a solicitação deve passar por análise humana.

---

# 10. Mudança de status

A solicitação deve seguir o fluxo:
```text
ABERTA
   ↓
EM ANÁLISE
   ↓
EM PROCESSO
   ↓
SOLUÇÃO
```

### ABERTA
A solicitação foi registrada, mas ainda não passou pela análise necessária.

### EM ANÁLISE
A solicitação está sendo analisada para determinar impacto, urgência, prioridade e encaminhamento.

### EM PROCESSO
A equipe responsável já iniciou o tratamento.

### SOLUÇÃO
O tratamento foi concluído e a solução foi registrada.

---

# 11. Rastreabilidade
Toda alteração relevante na decisão deve deixar um registro.

O histórico deve permitir responder:

> **O que foi decidido?**
> **Quando foi decidido?**
> **Quem tomou ou alterou a decisão?**
> **O que mudou?**
> **Por que mudou?**

Essa informação será importante principalmente quando uma classificação automática for posteriormente alterada por uma pessoa.

---

# 12. Princípio central

A regra mais importante do projeto é:

> **O sistema deve ajudar a organizar a decisão, não inventar uma decisão quando não possui informações suficientes.**

Por isso, a revisão humana faz parte do próprio funcionamento do sistema e não deve ser tratada como uma exceção criada depois da implementação.
