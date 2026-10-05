## Purpose

Define uma interface gráfica interativa para tornar visíveis o mapa, os drones, os turnos e as restrições de capacidade sem misturar apresentação com o algoritmo de roteamento.

## ADDED Requirements

### Requirement: Render the map spatially

A interface SHALL representar cada zona como um elemento 2D posicionado pelas coordenadas do mapa e cada conexão como uma ligação visual entre as zonas.

#### Scenario: Show a loaded map

- **WHEN** o usuário abre um mapa válido com a opção gráfica
- **THEN** a janela mostra todas as zonas acessíveis, zonas bloqueadas e conexões conhecidas em uma cena navegável

#### Scenario: Show zone state

- **WHEN** uma zona possui tipo, cor ou capacidade configurada
- **THEN** o elemento visual diferencia o tipo, aplica uma cor disponível e exibe sua ocupação quando aplicável

### Requirement: Visualize drone movement by turn

A interface SHALL mostrar a posição dos drones e atualizar a cena de acordo com os frames produzidos pela simulação.

#### Scenario: Advance one turn

- **WHEN** o usuário aciona o comando de próximo turno
- **THEN** a interface aplica exatamente o próximo frame, atualiza as posições e informa o número do turno

#### Scenario: Animate a restricted movement

- **WHEN** um drone está em trânsito para uma zona restricted
- **THEN** a interface representa o drone na conexão ou em estado de trânsito até sua chegada no frame correto

### Requirement: Provide simulation controls

A interface SHALL oferecer controles de iniciar, pausar, avançar um turno, reiniciar e ajustar a velocidade da animação.

#### Scenario: Pause and resume

- **WHEN** o usuário pausa uma simulação em execução
- **THEN** nenhum frame novo é aplicado até que o usuário retome ou avance manualmente

#### Scenario: Reset simulation

- **WHEN** o usuário seleciona reiniciar
- **THEN** a cena retorna ao estado inicial e o contador de turnos volta ao primeiro frame

### Requirement: Show simulation details

A interface SHALL exibir o turno atual, movimentos do turno, estado dos drones e uso das capacidades relevantes.

#### Scenario: Inspect a turn

- **WHEN** um frame é aplicado
- **THEN** o painel mostra os movimentos ocorridos e os valores usados/máximos das zonas e conexões relevantes

### Requirement: Preserve headless execution

A interface SHALL ser opcional e não SHALL alterar a saída oficial nem exigir PySide6 para executar o modo terminal.

#### Scenario: Run without GUI

- **WHEN** o usuário executa o CLI sem `--gui`
- **THEN** o programa produz a saída terminal atual sem abrir uma janela gráfica

#### Scenario: Handle missing GUI dependency

- **WHEN** o usuário solicita `--gui` sem PySide6 instalado
- **THEN** o programa informa como instalar a dependência e encerra com erro controlado
