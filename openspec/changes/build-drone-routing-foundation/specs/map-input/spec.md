## Purpose

Define a leitura confiável dos mapas Fly-in, transformando sua sintaxe em uma rede validada e fornecendo erros claros para entradas que não podem ser simuladas.

## ADDED Requirements

### Requirement: Parse valid Fly-in maps

O sistema SHALL aceitar arquivos com `nb_drones`, exatamente um `start_hub`, exatamente um `end_hub`, zonas, conexões bidirecionais, metadados opcionais e comentários iniciados por `#`.

#### Scenario: Parse a valid map

- **WHEN** o sistema recebe um mapa válido dos diretórios `easy`, `medium`, `hard` ou `challenger`
- **THEN** ele cria uma rede com o número de drones, zonas, conexões, zona inicial e zona final correspondentes ao arquivo

#### Scenario: Apply default metadata

- **WHEN** uma zona não informa tipo, cor ou `max_drones`, ou uma conexão não informa `max_link_capacity`
- **THEN** o sistema aplica respectivamente `normal`, ausência de cor, capacidade de zona `1` e capacidade de conexão `1`

#### Scenario: Ignore comments and blank lines

- **WHEN** o arquivo contém comentários ou linhas vazias
- **THEN** essas linhas não alteram a rede produzida

### Requirement: Reject invalid map definitions

O sistema SHALL rejeitar uma entrada inválida com uma mensagem clara que identifique a linha e a causa do erro.

#### Scenario: Reject invalid capacities

- **WHEN** `nb_drones`, `max_drones` ou `max_link_capacity` não é um inteiro positivo
- **THEN** o parser interrompe a leitura e informa o campo e a linha inválida

#### Scenario: Reject invalid topology

- **WHEN** há zona duplicada, conexão duplicada, conexão para zona inexistente, tipo de zona inválido ou mais de um início/fim
- **THEN** o parser rejeita o mapa com uma mensagem específica

#### Scenario: Reject missing required declarations

- **WHEN** o arquivo não contém contagem de drones, `start_hub` ou `end_hub`
- **THEN** o parser rejeita o mapa e informa a declaração ausente
