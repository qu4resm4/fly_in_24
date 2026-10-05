## Context

O repositório atualmente contém o enunciado, a régua e mapas de entrada, mas nenhuma aplicação. O projeto exige Python 3.10+, orientação a objetos, tipagem, `flake8`, `mypy`, grafo próprio e saída por turnos. A simulação combina caminhos ponderados com capacidades de zonas e conexões e movimentos restritos de dois turnos.

## Goals / Non-Goals

**Goals:**

- Separar parsing, domínio, planejamento, simulação e apresentação.
- Construir o grafo com lista de adjacência própria.
- Obter uma solução correta e explicável antes de otimizações avançadas.
- Permitir que a saída oficial e a visualização sejam substituídas independentemente.
- Validar os mapas fornecidos e casos de erro por testes automatizados.

**Non-Goals:**

- Não criar interface gráfica nesta mudança.
- Não usar `networkx`, `graphlib` ou outra biblioteca de lógica de grafos.
- Não prometer o recorde do mapa challenger na primeira implementação.
- Não alterar os mapas ou o enunciado fornecidos.

## Decisions

### Modelo de domínio orientado a objetos

Serão usados objetos separados para zonas, conexões, drones, grafo, estado da simulação e eventos. Isso torna capacidades e invariantes explícitos e facilita a demonstração de OOP na avaliação. Uma coleção de dicionários sem encapsulamento foi descartada por dificultar validação e manutenção.

### Grafo próprio com lista de adjacência

O grafo manterá zonas por nome e vizinhos associados às conexões. A lista de adjacência oferece busca eficiente e atende à proibição de bibliotecas de grafos. Conexões serão normalizadas por um par de nomes para detectar duplicatas em qualquer direção.

### Planejamento em duas camadas

O planejador inicial usará busca de menor custo para obter rotas e uma política de distribuição com penalidade de congestionamento. A simulação fará a validação final por turno. Um planejador de fluxo mínimo expandido no tempo fica como evolução posterior, pois aumenta muito a complexidade antes de existir uma base correta.

### Atualização da simulação em duas fases

Cada turno será dividido em planejamento e aplicação. Primeiro são calculadas as saídas, reservas e entradas válidas; depois todas as mudanças são aplicadas juntas. Isso evita que a ordem dos drones altere indevidamente a capacidade disponível.

### Separação de saída

O formato oficial será produzido por um formatador próprio. Visualização e relatório de capacidade serão adaptadores opcionais, ativados por flags, para que informações decorativas não quebrem o avaliador automático.

### CLI e validação

O ponto de entrada aceitará um caminho de mapa e flags como `--visual` e `--capacity-info`. Erros de parsing, mapas desconectados e falhas de simulação serão convertidos em mensagens de usuário, sem traceback por padrão.

## Risks / Trade-offs

- [Otimização insuficiente em mapas difíceis] → medir turnos em todos os mapas e manter o modelo preparado para substituir o planejador por fluxo em rede temporal.
- [Ambiguidade de capacidade durante movimentos restritos] → modelar explicitamente drones em trânsito e testar entrada, permanência e chegada.
- [Cores ANSI confundirem testes] → manter a saída oficial sem cores por padrão e tornar a visualização opt-in.
- [Erros de tipagem aparecerem tarde] → executar `flake8` e `mypy` desde a criação dos primeiros módulos.

## Migration Plan

1. Criar a estrutura Python, configuração de ferramentas e testes.
2. Implementar parser e domínio, validando mapas Easy.
3. Implementar rotas e simulação, adicionando testes de capacidades e duração.
4. Adicionar saída oficial, visualização e `--capacity-info`.
5. Rodar lint, testes e todos os mapas; ajustar o planejador sem modificar o contrato dos mapas.

Como ainda não existe implementação, rollback consiste em remover os módulos da mudança e manter intactos o enunciado e os mapas originais.

## Open Questions

Nenhuma. As decisões necessárias para iniciar a implementação estão definidas; a escolha de um algoritmo de fluxo temporal é uma otimização posterior e não altera o contrato desta mudança.
