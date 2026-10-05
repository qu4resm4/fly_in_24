"""Smoke tests da interface PySide6 sem exigir uma tela física."""

from __future__ import annotations

import os
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

try:
    from PySide6.QtWidgets import QApplication
except ImportError:  # pragma: no cover - depende do ambiente de execução
    QApplication = None  # type: ignore[assignment,misc]

from fly_in.parser import MapParser  # noqa: E402
from fly_in.routing import RoutePlanner  # noqa: E402
from fly_in.simulation import Simulation  # noqa: E402
from fly_in.visualization.frames import create_frames  # noqa: E402
from fly_in.visualization.gui import SimulationWindow  # noqa: E402


@unittest.skipIf(QApplication is None, "PySide6 não instalado")
class GuiTests(unittest.TestCase):
    """Verifica a construção e os controles básicos da janela."""

    def test_window_can_advance_and_reset(self) -> None:
        root = Path(__file__).parents[1]
        count, graph, start, goal = MapParser().parse(root / "maps/easy/02_simple_fork.txt")
        routes = RoutePlanner(graph).plan_routes(start, goal, count)
        turns = Simulation(graph, start, goal, routes).run()
        frames = create_frames(graph, start, count, turns)
        app = QApplication.instance() or QApplication([])
        window = SimulationWindow(graph, frames)
        window.next_frame()
        self.assertEqual(window.frame_index, 1)
        window.reset()
        self.assertEqual(window.frame_index, 0)
        window.close()
        app.processEvents()
