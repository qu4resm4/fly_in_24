## Purpose

Define uma saída compreensível para acompanhar os turnos, posições e capacidades da simulação sem comprometer o formato oficial usado pelos testes automáticos.

## ADDED Requirements

### Requirement: Produce official turn output

O sistema SHALL oferecer uma saída padrão em que cada linha representa um turno e cada movimento segue `D<ID>-<zona>` ou `D<ID>-<conexão>`.

#### Scenario: Print moving drones only

- **WHEN** um turno é executado
- **THEN** a linha contém somente drones que se moveram naquele turno, separados por espaços

#### Scenario: Keep output compatible

- **WHEN** a simulação termina
- **THEN** a saída padrão contém apenas os turnos até a entrega do último drone, sem linhas extras de visualização

### Requirement: Show optional colored visualization

O sistema SHALL oferecer um modo opcional de visualização terminal que mostre turnos, posições dos drones e cores associadas às zonas.

#### Scenario: Visualize a turn

- **WHEN** o usuário ativa `--visual`
- **THEN** o terminal mostra o turno corrente, as posições ou movimentos dos drones e uma representação legível da rede

#### Scenario: Handle arbitrary color names

- **WHEN** um mapa informa uma cor sem equivalente ANSI conhecido
- **THEN** a visualização continua funcionando usando uma cor padrão ou sem cor para aquela zona

### Requirement: Show capacity information

O sistema SHALL oferecer `--capacity-info` para exibir, durante a simulação, ocupação atual e capacidade das zonas e conexões relevantes.

#### Scenario: Report capacities

- **WHEN** o usuário executa a simulação com `--capacity-info`
- **THEN** a saída informa valores usados e máximos para zonas e conexões em cada turno
