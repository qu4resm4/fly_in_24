## Why

A implementação atual encontra rotas de menor custo e distribui rotas equivalentes, mas ainda não considera adequadamente a capacidade e o tempo de passagem ao escolher rotas para cada drone. Isso produz soluções válidas, porém subótimas nos mapas Hard e Challenger.

## What Changes

- Adicionar planejamento consciente de gargalos de zonas e conexões.
- Avaliar o tempo de chegada e a ocupação prevista ao distribuir drones.
- Preservar a validação de capacidades e o formato de saída existentes.
- Adicionar métricas de turnos e testes de regressão para os mapas complexos.

## Capabilities

### New Capabilities

- `capacity-aware-routing`: planejamento de rotas considerando custo, capacidade e congestionamento previsto.

### Modified Capabilities

Nenhuma.

## Impact

- Alteração do planejador em `src/fly_in/routing.py` e da integração da CLI.
- Novos testes de distribuição e desempenho.
- Nenhuma dependência externa de grafos.
