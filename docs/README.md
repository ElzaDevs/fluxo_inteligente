# Sistema de Triagem e Priorização de Solicitações Internas

## Sobre o projeto

Este projeto nasceu de um problema comum em empresas: **muitas solicitações precisam ser tratadas, mas nem sempre chegam organizadas ou com clareza sobre o que deve ser atendido primeiro.**

Quando isso acontece, podem surgir atrasos, encaminhamentos incorretos, perda de prazos e dificuldade para identificar situações que realmente exigem atenção.

A proposta deste projeto é criar um sistema capaz de transformar uma solicitação desorganizada em um processo de triagem estruturado.

O sistema analisa **impacto e urgência**, define uma prioridade, indica o setor responsável e permite revisão humana quando as informações não forem suficientes para uma decisão segura.

---

## O problema

Uma solicitação interna pode envolver desde uma necessidade simples de uma área até uma situação capaz de afetar processos importantes ou a empresa inteira.

O problema não está apenas em receber essas solicitações.

O desafio é **entender cada situação, diferenciar sua urgência do seu impacto e encaminhá-la corretamente.**

---

## A proposta

O sistema organiza esse processo em etapas:

```text
RECEBER
   ↓
IDENTIFICAR
   ↓
AVALIAR IMPACTO
   +
AVALIAR URGÊNCIA
   ↓
CLASSIFICAR
   ↓
ENCAMINHAR
   ↓
ACOMPANHAR
   ↓
REGISTRAR SOLUÇÃO
```

Quando não houver informação suficiente para uma classificação segura:

```text
CLASSIFICAR
   ↓
REVISÃO HUMANA
   ↓
NOVA DECISÃO
```

A ideia é usar automação para **apoiar a triagem**, e não simplesmente automatizar decisões sem considerar o contexto.

---

## Prioridade

As solicitações serão organizadas em quatro níveis:

| Código | Prioridade |
| ------ | ---------- |
| A      | Crítica    |
| B      | Média      |
| C      | Alta       |
| D      | Baixa      |

Os critérios para cada classificação fazem parte das regras de negócio do projeto.

---

## Fluxo da solicitação

Depois de registrada, a solicitação percorre o seguinte ciclo:

```text
ABERTA
  ↓
EM ANÁLISE
  ↓
EM PROCESSO
  ↓
SOLUÇÃO
```

Durante esse processo, o sistema mantém o histórico das principais decisões.

---

## Quem utiliza

O projeto considera quatro participantes principais:

* **Solicitante:** registra a situação e acompanha seu andamento.
* **Analista de triagem:** analisa impacto, urgência, prioridade e encaminhamento.
* **Gestor:** acompanha situações relevantes e o andamento das solicitações.
* **Equipe responsável:** recebe a solicitação, trabalha na resolução e registra a solução.

---

## Setores envolvidos

A primeira versão considera como possíveis destinos:

* Gestão da Economia;
* Analistas de Suporte;
* Setor Financeiro;
* Tecnologia da Informação.

A estrutura foi pensada para permitir a inclusão de outros setores posteriormente.

---

## O que estou praticando neste projeto

Mais do que desenvolver uma aplicação, este projeto está sendo construído para praticar uma visão completa de Engenharia de Software:

* levantamento e organização de requisitos;
* identificação de regras de negócio;
* modelagem de processos;
* definição de fluxos;
* tomada de decisão baseada em critérios;
* rastreabilidade;
* separação entre regra de negócio e implementação;
* testes;
* arquitetura de software;
* uso responsável de automação e IA.

---

## Estrutura da documentação

```text
docs/
├── problema.md
├── requisitos.md
├── usuarios.md
├── fluxo.md
├── regras-negocio.md
└── arquitetura.md
```

Cada documento representa uma parte diferente do projeto:

* `problema.md` → por que o sistema existe;
* `requisitos.md` → o que o sistema precisa fazer;
* `usuarios.md` → quem participa do processo;
* `fluxo.md` → como uma solicitação percorre o sistema;
* `regras-negocio.md` → como as decisões de negócio serão tomadas;
* `arquitetura.md` → como a solução será organizada tecnicamente.

---
## Próximos passos

A implementação será construída depois que as regras de negócio estiverem definidas.

A próxima etapa é detalhar **como impacto e urgência serão avaliados, como cada prioridade será determinada e em quais situações a decisão deverá obrigatoriamente passar por revisão humana.**
