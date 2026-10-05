# Fly-in

## Description

Fly-in é um simulador de roteamento de drones em uma rede de zonas conectadas. O programa lê um mapa, encontra rotas entre `start_hub` e `end_hub` e movimenta vários drones em turnos, respeitando custos de movimento, capacidade das zonas, capacidade das conexões e zonas bloqueadas.

A implementação usa um grafo próprio e não depende de `networkx`, `graphlib` ou outra biblioteca de lógica de grafos.

## Instructions

O projeto exige Python 3.10 ou superior. Para instalar em um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
make install
```

Executar um mapa:

```bash
make run
PYTHONPATH=src python3 -m fly_in.cli maps/easy/01_linear_path.txt
```

Opções de visualização:

```bash
PYTHONPATH=src python3 -m fly_in.cli --visual maps/easy/02_simple_fork.txt
PYTHONPATH=src python3 -m fly_in.cli --capacity-info maps/easy/03_basic_capacity.txt

# Interface gráfica PySide6
python3 -m pip install -e '.[gui]'
PYTHONPATH=src python3 -m fly_in.cli --gui maps/easy/02_simple_fork.txt
```

Na interface gráfica, use `Play`/`Pause` para iniciar ou parar a animação,
`Próximo turno` para avançar manualmente, `Reset` para voltar ao estado inicial
e o controle de velocidade para ajustar o intervalo entre frames. A GUI é
opcional; se PySide6 não estiver instalado, o modo terminal continua disponível.

Verificações locais:

```bash
make test
make lint
make clean
```

## Algorithm explanation

O mapa é armazenado como uma lista de adjacência construída manualmente. O planejador percorre caminhos simples e calcula o custo pela zona de destino: zonas normais e prioritárias custam um turno, enquanto zonas restritas custam dois; zonas bloqueadas são ignoradas.

O planejador enumera rotas simples candidatas, calcula custo e vazão mínima de cada uma e atribui os drones incrementalmente à rota com menor tempo estimado de conclusão. Assim, caminhos equivalentes são distribuídos e caminhos um pouco mais longos podem ser usados quando possuem maior vazão. A simulação executa cada turno em duas fases: primeiro reserva movimentos compatíveis com as capacidades e depois aplica todos os movimentos simultaneamente. Drones que não podem avançar aguardam. Uma zona restrita mantém o drone em trânsito por um turno e exige chegada no turno seguinte. A execução compara essa estratégia com o baseline de menor caminho e mantém a solução com menos turnos.

Essa primeira versão prioriza correção e explicabilidade. Um planejador de fluxo mínimo em grafo expandido no tempo é uma possível otimização para reduzir ainda mais os turnos em mapas complexos.

## Visual representation

O modo padrão imprime somente o formato oficial, uma linha por turno:

```text
D1-waypoint1 D2-waypoint1
D1-waypoint2 D2-waypoint2
D1-goal D2-goal
```

`--visual` adiciona um mapa textual colorido, o turno e os movimentos. `--capacity-info` informa ocupação e capacidade das zonas e conexões. A visualização é opcional para não interferir nos testes automáticos do formato oficial.

## Project structure

```text
src/fly_in/
├── models.py      # zonas, conexões, drones e grafo
├── parser.py      # leitura e validação do mapa
├── routing.py     # planejamento de rotas
├── simulation.py  # execução por turnos
├── output.py      # saída oficial e visualização
└── cli.py         # interface de linha de comando
```

## Example input

```text
nb_drones: 1
start_hub: start 0 0 [color=green]
hub: middle 1 0 [zone=priority color=blue]
end_hub: goal 2 0 [color=red]
connection: start-middle
connection: middle-goal
```

Expected output:

```text
D1-middle
D1-goal
```
