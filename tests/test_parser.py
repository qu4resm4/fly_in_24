"""Testes do parser e do grafo."""

import tempfile
import unittest
from pathlib import Path

from fly_in.parser import MapParseError, MapParser


class ParserTests(unittest.TestCase):
    """Verifica entradas válidas e inválidas."""

    def test_parse_easy_map(self) -> None:
        root = Path(__file__).parents[1]
        count, graph, start, goal = MapParser().parse(root / "maps/easy/01_linear_path.txt")
        self.assertEqual(count, 2)
        self.assertEqual((start, goal), ("start", "goal"))
        self.assertEqual(len(graph.zones), 4)

    def test_reject_missing_start(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as file:
            file.write("nb_drones: 1\nend_hub: goal 0 0\n")
            file.flush()
            with self.assertRaises(MapParseError):
                MapParser().parse(file.name)

    def test_reject_invalid_capacity(self) -> None:
        content = """nb_drones: 1
start_hub: start 0 0
end_hub: goal 1 0
connection: start-goal [max_link_capacity=0]
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as file:
            file.write(content)
            file.flush()
            with self.assertRaisesRegex(MapParseError, "linha 4"):
                MapParser().parse(file.name)
