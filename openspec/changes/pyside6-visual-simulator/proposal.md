## Why

O modo terminal já permite acompanhar os movimentos, mas não comunica facilmente a estrutura espacial do mapa, a ocupação das zonas e a evolução dos drones entre turnos. Uma interface gráfica torna a simulação mais demonstrável e facilita a compreensão dos conflitos e gargalos durante a avaliação.

## What Changes

- Adicionar uma interface desktop em PySide6.
- Desenhar zonas, conexões e drones em uma cena 2D usando as coordenadas do mapa.
- Animar a simulação turno a turno com play, pause, avanço, reset e controle de velocidade.
- Exibir painel lateral com turno, estado dos drones, capacidades e movimentos.
- Manter o modo terminal e a saída oficial sem dependência da interface gráfica.
- Adicionar testes para o modelo de frames e um smoke test da aplicação.

## Capabilities

### New Capabilities

- `desktop-visualization`: interface gráfica interativa da simulação Fly-in.

### Modified Capabilities

Nenhuma.

## Impact

- Nova dependência opcional de desenvolvimento/execução: PySide6.
- Novos módulos de apresentação em `src/fly_in/visualization/`.
- Pequena adaptação no CLI para ativar a interface com `--gui`.
- O motor, parser, planejador e formato terminal continuam independentes da GUI.
