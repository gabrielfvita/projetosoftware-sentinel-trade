# SentinelTrade - Regra de Ordem Limitada

Esta especificação complementa os diagramas UML e os casos de uso CSU04, CSU05, CSU10 e CSU11.

## Semântica do preço

O campo `preco` da ordem representa o **preço limite** informado pelo investidor, e não o preço garantido de execução.

- **Compra:** a ordem pode ser executada quando `cotação atual <= preço limite`.
- **Venda:** a ordem pode ser executada quando `cotação atual >= preço limite`.
- Quando a condição não é atendida, a ordem permanece no estado **enviada**, sem alterar saldo ou carteira.
- Quando a condição é atendida, a execução financeira utiliza a **cotação de mercado vigente**.
- O sistema registra `quantidade_executada` e `preco_medio_execucao`.
- Em execução parcial, a ordem permanece `parcialmente_executada` até nova execução do saldo restante ou cancelamento.

## Exemplo

Cotação de PETR4: R$ 38,50.

- Venda limitada a R$ 50,00: permanece `enviada` aguardando preço.
- Venda limitada a R$ 35,00: pode executar a R$ 38,50.
- Compra limitada a R$ 40,00: pode executar a R$ 38,50.
- Compra limitada a R$ 30,00: permanece `enviada` aguardando preço.
