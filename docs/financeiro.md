# Módulo Financeiro

O módulo financeiro permite que cada empresa cadastre e consulte seus próprios lançamentos.

## Lançamento

Cada lançamento possui:

- tipo: RECEITA ou DESPESA;
- descrição;
- categoria;
- valor;
- data;
- status: REALIZADO ou PENDENTE;
- observações.

## Dashboard

Os indicadores são calculados a partir dos dados persistidos, sem valores fictícios:

- receitas realizadas;
- despesas realizadas;
- saldo;
- despesas pendentes;
- quantidade de lançamentos;
- evolução mensal;
- despesas por categoria;
- lançamentos recentes.

## Importação

A empresa pode carregar um CSV para cadastrar vários registros.

O formato esperado é:

```csv
tipo,descricao,categoria,valor,data_lancamento,status,observacoes
RECEITA,Contrato A,Vendas,"1250,50",2026-09-10,REALIZADO,Cliente A
DESPESA,Internet,Infraestrutura,120.00,2026-09-11,REALIZADO,Fornecedor
```

O parser aceita valores no padrão brasileiro com vírgula decimal e também valores usando ponto decimal.

## Isolamento multiempresa

Todo lançamento possui `empresa_id`.

As consultas por ID, listagem, dashboard, edição e exclusão filtram pela empresa do usuário autenticado. Isso evita que um usuário consulte ou altere dados de outra organização.
