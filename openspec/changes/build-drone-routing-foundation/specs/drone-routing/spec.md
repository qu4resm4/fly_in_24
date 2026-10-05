## Purpose

Define o planejamento e a execução da movimentação de todos os drones até o destino, respeitando custos, capacidades, conflitos e o tempo discreto da simulação.

## ADDED Requirements

### Requirement: Find valid routes

O sistema SHALL encontrar uma rota válida do início ao fim quando existir caminho acessível, considerando zonas bloqueadas, custo de zonas restritas e preferência por zonas prioritárias.

#### Scenario: Route a linear map

- **WHEN** o sistema recebe um mapa linear com um ou mais drones
- **THEN** cada drone é encaminhado ao destino sem entrar em zona bloqueada ou exceder capacidades

#### Scenario: Avoid dead ends and loops

- **WHEN** o mapa possui becos sem saída ou ciclos
- **THEN** o planejamento não entra em loop infinito e escolhe uma rota que alcança o destino quando ela existe

#### Scenario: Report disconnected maps

- **WHEN** não existe caminho acessível entre início e destino
- **THEN** a execução termina com erro informativo e não produz uma simulação incompleta

### Requirement: Simulate simultaneous movements

O sistema SHALL executar a simulação em turnos, planejando movimentos simultâneos e omitindo drones que permanecem parados da saída daquele turno.

#### Scenario: Respect zone capacity

- **WHEN** vários drones tentam entrar na mesma zona no mesmo turno
- **THEN** no máximo a capacidade disponível da zona é utilizada, considerando também drones que saem naquele turno

#### Scenario: Respect connection capacity

- **WHEN** vários drones tentam atravessar a mesma conexão no mesmo turno
- **THEN** no máximo `max_link_capacity` drones iniciam a travessia naquela conexão

#### Scenario: Wait when blocked

- **WHEN** um drone não pode avançar sem violar uma capacidade
- **THEN** ele permanece em sua posição e pode avançar em um turno posterior

### Requirement: Handle movement durations

O sistema SHALL tratar movimentos para zonas `restricted` como travessias de dois turnos, sem permitir pausa durante a travessia.

#### Scenario: Complete restricted movement

- **WHEN** um drone inicia movimento para uma zona restrita
- **THEN** ele ocupa a conexão durante o trânsito, chega no turno seguinte e a saída representa a conexão enquanto estiver em trânsito

#### Scenario: Finish all deliveries

- **WHEN** todos os drones chegam à zona final
- **THEN** a simulação encerra imediatamente e não produz turnos adicionais
