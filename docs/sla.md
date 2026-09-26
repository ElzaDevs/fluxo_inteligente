# SLA de referência — simulação empresarial

Este projeto utiliza uma política de SLA de referência para simular um cenário de gestão de serviços corporativos. Os números abaixo não representam contrato ou política oficial de uma empresa.

A modelagem foi inspirada em mecanismos comuns de plataformas ITSM: metas distintas de resposta e resolução, calendários de atendimento e condições de início, pausa e encerramento do relógio.

## Política do MVP

| Prioridade | Resposta | Resolução | Calendário |
|---|---:|---:|---|
| A — Crítica | 15 min | 4 h | 24x7 |
| B — Alta | 30 min | 8 h | 24x7 |
| C — Média | 4 h úteis | 24 h úteis | Seg–Sex, 09:00–18:00, intervalo 12:00–13:00 |
| D — Baixa | 8 h úteis | 40 h úteis | Seg–Sex, 09:00–18:00, intervalo 12:00–13:00 |

Os valores são dados de demonstração. Em um ambiente real, seriam parametrizados conforme serviço, contrato, criticidade, horário de suporte e objetivos acordados.

## Ciclo do SLA

### Início

O SLA é criado no momento do registro e associado à prioridade resultante da triagem.

### Resposta

Mede o tempo até a primeira resposta ou assunção do atendimento.

### Resolução

Mede o tempo até a conclusão da solicitação.

### Pausa

O relógio pode ser pausado quando o atendimento está bloqueado por uma dependência externa:

- aguardando solicitante;
- aguardando terceiro;
- aguardando aprovação.

A pausa fica registrada no histórico e o relógio é retomado quando a solicitação volta para EM_PROCESSO.

Esse comportamento é usado em ferramentas ITSM para evitar que períodos fora do controle da equipe sejam contados indevidamente contra a meta.

### Encerramento

Quando a solicitação entra em SOLUCAO, o sistema registra se a meta de resolução foi cumprida ou violada.

## Escalonamento

Uma evolução natural deste projeto é adicionar alertas automáticos em marcos como 50%, 75% e 90% do SLA, além da abertura de escalonamento no vencimento.

## Por que o modelo é mais realista?

O SLA deixa de ser apenas um número fixo e passa a possuir:

- prioridade;
- resposta;
- resolução;
- calendário;
- pausa;
- retomada;
- histórico;
- cumprimento ou violação.

Esses elementos correspondem a conceitos documentados em plataformas de gestão de serviços como ServiceNow e Jira Service Management.
