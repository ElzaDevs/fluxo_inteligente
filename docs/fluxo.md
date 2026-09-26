# Fluxo da solicitação

~~~text
REGISTRO
   |
   v
ABERTA
   |
   v
TRIAGEM
   |
   +---- dados suficientes? ---- não ----> REVISÃO HUMANA
   |                                      |
   |                                      v
   +------------------------------------ DECISÃO
   |
   v
PRIORIDADE
   |
   v
SLA
   |
   v
ENCAMINHAMENTO
   |
   v
EM ANÁLISE
   |
   v
EM PROCESSO
   |
   v
SOLUÇÃO
~~~

## Caminho automático

Quando impacto, urgência e categoria são suficientes, o sistema calcula prioridade, SLA e setor.

## Caminho de revisão

Quando faltam dados ou a categoria não permite determinar o setor, a solicitação recebe revisão humana.

A revisão permite corrigir impacto, urgência, prioridade e setor, mantendo justificativa no histórico.
