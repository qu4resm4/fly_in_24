## Purpose

Define como o planejador deve distribuir drones entre rotas alternativas levando em conta gargalos, capacidades e tempo estimado de entrega.

## ADDED Requirements

### Requirement: Prefer capacity-aware route assignments

O sistema SHALL considerar custo de movimento, capacidade de zonas, capacidade de conexões e congestionamento previsto ao atribuir rotas aos drones.

#### Scenario: Distribute equivalent paths

- **WHEN** existem duas ou mais rotas de custo equivalente com capacidades disponíveis
- **THEN** os drones são distribuídos entre elas quando isso reduz ou mantém o tempo total de simulação

#### Scenario: Avoid a narrow bottleneck when useful

- **WHEN** uma rota curta contém um gargalo e uma rota ligeiramente mais longa possui maior vazão
- **THEN** o planejador pode escolher a rota mais longa para drones adicionais quando o tempo estimado total for menor

### Requirement: Preserve valid simulation constraints

O sistema SHALL produzir somente atribuições que possam ser executadas pelo simulador respeitando zonas bloqueadas, capacidades e movimentos restritos.

#### Scenario: Keep restricted movement valid

- **WHEN** uma rota contém uma zona restricted
- **THEN** a estimativa e a atribuição contabilizam o custo de dois turnos e não permitem pausa durante o trânsito

#### Scenario: Keep impossible maps rejected

- **WHEN** não existe rota acessível até o destino
- **THEN** o planejador informa que não há solução em vez de produzir rotas inválidas

### Requirement: Expose measurable planning results

O sistema SHALL permitir medir a quantidade de turnos da simulação para comparar o resultado do planejador em diferentes mapas.

#### Scenario: Compare complex maps

- **WHEN** um mapa Hard ou Challenger é executado
- **THEN** o resultado informa ou permite contar os turnos até a entrega do último drone
