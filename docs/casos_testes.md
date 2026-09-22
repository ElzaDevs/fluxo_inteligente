# Casos de teste das regras de negócio
Estes casos verificam se a triagem está produzindo a prioridade esperada a partir do impacto e da urgência.
O objetivo é validar a regra de negócio antes de transformá-la em código.

---

## CT-01 — Solicitação de baixo impacto e baixa urgência

**Situação:**
Uma solicitação afeta apenas uma atividade de uma área e não possui prazo próximo.
**Impacto:** Baixo
**Urgência:** Baixa
**Prioridade esperada:** D
**Resultado esperado:**
A solicitação pode ser planejada para atendimento posterior.

---

## CT-02 — Baixo impacto e urgência média

**Situação:**
Uma atividade específica está com dificuldade para funcionar, mas existe um prazo para correção.
**Impacto:** Baixo
**Urgência:** Média
**Prioridade esperada:** D
**Resultado esperado:**
A solicitação deve ser acompanhada, mas não apresenta características de uma situação prioritária.

---

## CT-03 — Baixo impacto e urgência alta
**Situação:**
Uma atividade específica precisa ser resolvida rapidamente devido a um prazo próximo.
**Impacto:** Baixo
**Urgência:** Alta
**Prioridade esperada:** C
**Resultado esperado:**
A necessidade de rapidez aumenta a prioridade, mas o baixo impacto impede que a situação seja tratada como crítica.

---

## CT-04 — Impacto médio e urgência média

**Situação:**
Um processo de uma área está prejudicado e existe prazo para normalização, mas ainda há margem para atuação.

**Impacto:** Médio
**Urgência:** Média
**Prioridade esperada:** C
**Resultado esperado:**
A solicitação deve receber acompanhamento e atendimento planejado.

---

## CT-05 — Impacto médio e urgência crítica
**Situação:**
Um problema afeta uma área importante e existe risco de consequência relevante caso não seja resolvido imediatamente.

**Impacto:** Médio
**Urgência:** Crítica
**Prioridade esperada:** B
**Resultado esperado:**
A solicitação deve receber atenção rápida.

---

## CT-06 — Alto impacto e baixa urgência

**Situação:**
Um problema afeta várias áreas ou um processo relevante, mas existe tempo suficiente para organizar o atendimento.

**Impacto:** Alto
**Urgência:** Baixa
**Prioridade esperada:** C
**Resultado esperado:**
A solicitação não deve ser ignorada devido ao seu impacto, mesmo sem urgência imediata.

---

## CT-07 — Alto impacto e alta urgência

**Situação:**
Um problema afeta várias áreas e precisa ser tratado rapidamente.
**Impacto:** Alto
**Urgência:** Alta
**Prioridade esperada:** B
**Resultado esperado:**
A solicitação deve receber atenção prioritária.

---

## CT-08 — Alto impacto e urgência crítica

**Situação:**
Uma situação afeta processos importantes da empresa e o atraso pode gerar consequência grave.
**Impacto:** Alto
**Urgência:** Crítica
**Prioridade esperada:** A
**Resultado esperado:**
A solicitação deve ser tratada como crítica.

---

## CT-09 — Impacto crítico e baixa urgência
**Situação:**
Existe risco de impacto amplo para a empresa, mas a consequência não ocorrerá imediatamente.

**Impacto:** Crítico
**Urgência:** Baixa
**Prioridade esperada:** B
**Resultado esperado:**
A situação não deve ser classificada como baixa prioridade apenas porque existe tempo para agir.

---

## CT-10 — Impacto crítico e urgência alta

**Situação:**
Um problema pode afetar a empresa de forma ampla e precisa ser tratado rapidamente.
**Impacto:** Crítico
**Urgência:** Alta
**Prioridade esperada:** A

**Resultado esperado:**
A solicitação deve receber prioridade crítica.

---

## CT-11 — Impacto crítico e urgência crítica

**Situação:**
Uma situação pode comprometer um processo essencial da empresa e exige ação imediata.
**Impacto:** Crítico
**Urgência:** Crítica
**Prioridade esperada:** A

**Resultado esperado:**
A solicitação deve ser tratada imediatamente como crítica.

---

## CT-12 — Informações insuficientes
**Situação:**
A descrição da solicitação não permite determinar com segurança o impacto ou a urgência.
**Impacto:** Indeterminado
**Urgência:** Indeterminada
**Prioridade:** Não definida
**Resultado esperado:**
A solicitação deve ser encaminhada para **REVISÃO HUMANA**.

O sistema não deve escolher uma prioridade apenas para completar o processo.

---
## CT-13 — Informações conflitantes

**Situação:**
A solicitação informa que o problema afeta apenas uma atividade, mas também indica possível interrupção de um processo utilizado por várias áreas.

**Impacto:** Conflitante
**Urgência:** A definir
**Prioridade:** Não definida
**Resultado esperado:**
A solicitação deve passar por **REVISÃO HUMANA** antes da classificação.

---

## CT-14 — Setor não identificado
**Situação:**
O sistema consegue determinar impacto, urgência e prioridade, mas não consegue identificar com segurança qual setor deve tratar a solicitação.

**Prioridade:** Definida
**Setor:** Indeterminado
**Resultado esperado:**
A prioridade permanece registrada, mas o encaminhamento deve passar por análise humana.

---

# Resultado esperado dos testes
Os testes devem garantir principalmente quatro comportamentos:

1. **Impacto e urgência são analisados separadamente.**
2. **A prioridade considera os dois fatores.**
3. **Situações críticas recebem tratamento compatível com seu impacto.**
4. **Quando não existe informação suficiente, o sistema não inventa uma decisão.**
Esses casos servirão posteriormente como base para os testes automatizados da aplicação.