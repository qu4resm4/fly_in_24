"""Testes básicos de roteamento e simulação."""

import tempfile
import unittest
from pathlib import Path

from fly_in.parser import MapParser
from fly_in.routing import RoutePlanner
from fly_in.simulation import Simulation
from fly_in.visualization.frames import create_frames
from fly_in.visualization.gui import CoordinateMapper


class SimulationTests(unittest.TestCase):
    """Verifica que um mapa linear termina com todos os drones entregues."""

    def test_linear_map(self) -> None:
        root = Path(__file__).parents[1]
        count, graph, start, goal = MapParser().parse(root / "maps/easy/01_linear_path.txt")
        route = RoutePlanner(graph).shortest_path(start, goal)
        turns = Simulation(graph, start, goal, [route] * count).run()
        self.assertEqual(len(turns), 4)
        self.assertTrue(turns[-1].movements[-1].endswith("goal"))

    def test_restricted_zone_uses_transit_output(self) -> None:
        content = """nb_drones: 1
start_hub: start 0 0
hub: restricted 1 0 [zone=restricted]
end_hub: goal 2 0
connection: start-restricted
connection: restricted-goal
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as file:
            file.write(content)
            file.flush()
            _, graph, start, goal = MapParser().parse(file.name)
        route = RoutePlanner(graph).shortest_path(start, goal)
        turns = Simulation(graph, start, goal, [route]).run()
        self.assertTrue(
            any("start-restricted" in move for turn in turns for move in turn.movements)
        )

    def test_planner_distributes_equivalent_fork_paths(self) -> None:
        root = Path(__file__).parents[1]
        count, graph, start, goal = MapParser().parse(root / "maps/easy/02_simple_fork.txt")
        routes = RoutePlanner(graph).plan_routes(start, goal, count)
        self.assertEqual(len(routes), count)
        self.assertTrue(any("path_a" in route for route in routes))
        self.assertTrue(any("path_b" in route for route in routes))

    def test_frames_keep_initial_and_final_positions(self) -> None:
        root = Path(__file__).parents[1]
        count, graph, start, goal = MapParser().parse(root / "maps/easy/01_linear_path.txt")
        route = RoutePlanner(graph).shortest_path(start, goal)
        turns = Simulation(graph, start, goal, [route] * count).run()
        frames = create_frames(graph, start, count, turns)
        self.assertEqual(frames[0].positions[1], start)
        self.assertEqual(frames[-1].positions[1], goal)

    def test_coordinate_mapper_preserves_order(self) -> None:
        root = Path(__file__).parents[1]
        _, graph, _, _ = MapParser().parse(root / "maps/easy/01_linear_path.txt")
        mapper = CoordinateMapper(graph)
        first = mapper.point(0, 0)
        second = mapper.point(1, 0)
        self.assertGreater(second[0], first[0])
