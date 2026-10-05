"""Interface de linha de comando do Fly-in."""

from __future__ import annotations

import argparse
import sys

from .output import OutputFormatter, TerminalVisualizer
from .parser import MapParseError, MapParser
from .routing import NoRouteError, RoutePlanner
from .simulation import Simulation, SimulationError
from .visualization.frames import create_frames


def main(argv: list[str] | None = None) -> int:
    """Executa o programa e retorna um código de saída."""
    parser = argparse.ArgumentParser(description="Simula drones em um mapa Fly-in")
    parser.add_argument("map", help="caminho do arquivo de mapa")
    parser.add_argument("--visual", action="store_true", help="exibe visualização colorida")
    parser.add_argument("--capacity-info", action="store_true", help="exibe capacidades por turno")
    parser.add_argument("--gui", action="store_true", help="abre a interface gráfica PySide6")
    args = parser.parse_args(argv)
    try:
        count, graph, start, goal = MapParser().parse(args.map)
        planner = RoutePlanner(graph)
        optimized = Simulation(graph, start, goal, planner.plan_routes(start, goal, count)).run()
        baseline_route = planner.shortest_path(start, goal)
        baseline = Simulation(graph, start, goal, [baseline_route] * count).run()
        turns = optimized if len(optimized) <= len(baseline) else baseline
        if args.gui:
            from .visualization.gui import GuiUnavailableError, launch_gui

            frames = create_frames(graph, start, count, turns)
            try:
                return launch_gui(graph, frames)
            except GuiUnavailableError as error:
                raise SimulationError(str(error)) from error
        if args.visual or args.capacity_info:
            print(TerminalVisualizer().render(graph, turns, args.capacity_info))
        else:
            print(OutputFormatter.official(turns))
        return 0
    except (MapParseError, NoRouteError, SimulationError, OSError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
