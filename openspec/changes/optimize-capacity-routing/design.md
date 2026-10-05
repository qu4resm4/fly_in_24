## Context

A implementação atual enumera caminhos simples e escolhe os melhores pelo custo estático, distribuindo rotas equivalentes de forma cíclica. Ela não modela a vazão dos gargalos durante a atribuição, embora o simulador já imponha capacidades corretamente.

## Goals / Non-Goals

**Goals:**

- Medir o custo e a vazão estimada de cada rota candidata.
- Atribuir cada drone incrementalmente à rota que produz menor conclusão estimada.
- Manter a simulação como autoridade final sobre conflitos reais.
- Melhorar os mapas complexos sem adicionar biblioteca de grafos.

**Non-Goals:**

- Não implementar ainda um solver completo de min-cost max-flow.
- Não mudar o formato dos mapas ou da saída oficial.
- Não remover a estratégia atual de busca de caminhos simples.

## Decisions

### Pontuação de rota com vazão

Cada rota será pontuada por custo de movimento, capacidade mínima de suas zonas e conexões e uso já atribuído. A atribuição incremental escolherá a rota com menor tempo estimado de conclusão, usando custo e número de gargalos como desempates.

### Limite de candidatos

O planejador continuará limitando o número de caminhos simples avaliados para evitar explosão combinatória em mapas com muitos ciclos. O limite será explícito e testável.

### Simulação como verificação

Após o planejamento, a simulação continuará validando o comportamento turno a turno. Se uma estimativa for otimista, a execução deverá continuar correta, ainda que o benchmark não melhore.

## Risks / Trade-offs

- [Estimativa não representa todos os conflitos temporais] → validar sempre com a simulação e comparar regressões por mapa.
- [Enumeração de caminhos cresce em grafos densos] → limitar candidatos e podar ciclos.
- [Heurística pode piorar um mapa] → manter testes de turnos e comparar com a estratégia anterior.

## Migration Plan

1. Adicionar pontuação de vazão e atribuição incremental.
2. Comparar os turnos antes e depois em todos os mapas.
3. Manter a estratégia anterior como fallback se não houver candidatos válidos.
4. Executar lint, testes e OpenSpec.

## Open Questions

Nenhuma.
