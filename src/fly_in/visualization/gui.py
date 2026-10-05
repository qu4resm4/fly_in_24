"""Janela PySide6 para visualizar a simulação Fly-in."""

from __future__ import annotations

from typing import Any

from ..models import Graph
from .frames import SimulationFrame


class GuiUnavailableError(RuntimeError):
    """Indica que PySide6 não está instalado."""


def launch_gui(graph: Graph, frames: list[SimulationFrame]) -> int:
    """Abre a janela gráfica e bloqueia até seu encerramento."""
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError as error:
        raise GuiUnavailableError(
            "PySide6 não está instalado; use `pip install -e '.[gui]'`"
        ) from error
    app = QApplication.instance() or QApplication([])
    window = SimulationWindow(graph, frames)
    window.show()
    return int(app.exec())


try:
    from PySide6.QtCore import QTimer, Qt
    from PySide6.QtGui import QBrush, QColor, QPen
    from PySide6.QtWidgets import (
        QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsScene, QGraphicsTextItem,
        QGraphicsView, QHBoxLayout, QLabel, QMainWindow, QPushButton, QSlider,
        QScrollArea, QVBoxLayout, QWidget,
    )
except ImportError:  # pragma: no cover - dependência opcional
    QTimer = Any  # type: ignore[misc,assignment]
    Qt = Any  # type: ignore[misc,assignment]
    QBrush = QColor = QPen = Any  # type: ignore[misc,assignment]
    QGraphicsEllipseItem = QGraphicsLineItem = QGraphicsScene = Any  # type: ignore[misc,assignment]
    QGraphicsTextItem = QGraphicsView = QHBoxLayout = QLabel = QMainWindow = Any  # type: ignore[misc,assignment]  # noqa: E501
    QScrollArea = Any  # type: ignore[misc,assignment]
    QPushButton = QSlider = QVBoxLayout = QWidget = Any  # type: ignore[misc,assignment]


class CoordinateMapper:
    """Converte coordenadas inteiras do mapa para pixels."""

    def __init__(self, graph: Graph, scale: float = 100.0, margin: float = 80.0) -> None:
        self.scale = scale
        self.margin = margin
        xs = [zone.x for zone in graph.zones.values()]
        ys = [zone.y for zone in graph.zones.values()]
        self.min_x = min(xs, default=0)
        self.max_y = max(ys, default=0)

    def point(self, x: float, y: float) -> tuple[float, float]:
        """Retorna ponto de cena com eixo vertical invertido."""
        return (
            self.margin + (x - self.min_x) * self.scale,
            self.margin + (self.max_y - y) * self.scale,
        )


class SimulationWindow(QMainWindow):
    """Janela principal com mapa, controles e detalhes do turno."""

    def __init__(self, graph: Graph, frames: list[SimulationFrame]) -> None:
        super().__init__()
        self.graph = graph
        self.frames = frames
        self.frame_index = 0
        self.mapper = CoordinateMapper(graph)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.turn_label = QLabel()
        self.details_label = QLabel()
        self.details_scroll = QScrollArea()
        self.play_button = QPushButton("Play")
        self.next_button = QPushButton("Próximo turno")
        self.reset_button = QPushButton("Reset")
        self.speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.speed_slider.setRange(1, 10)
        self.speed_slider.setValue(5)
        self.zone_items: dict[str, QGraphicsEllipseItem] = {}
        self.drone_items: dict[int, QGraphicsEllipseItem] = {}
        self.drone_labels: dict[int, QGraphicsTextItem] = {}
        self._setup_window()
        self._draw_graph()
        self._create_drones()
        self._apply_frame(self.frames[0])

    def _setup_window(self) -> None:
        """Configura layout e controles da janela."""
        self.setWindowTitle("Fly-in — Simulação de drones")
        self.resize(1100, 720)
        self.play_button.clicked.connect(self.toggle_play)
        self.next_button.clicked.connect(self.next_frame)
        self.reset_button.clicked.connect(self.reset)
        self.speed_slider.valueChanged.connect(self._update_interval)
        controls = QHBoxLayout()
        controls.addWidget(self.play_button)
        controls.addWidget(self.next_button)
        controls.addWidget(self.reset_button)
        controls.addWidget(QLabel("Velocidade"))
        controls.addWidget(self.speed_slider)
        side = QVBoxLayout()
        side.addWidget(self.turn_label)
        self.details_label.setWordWrap(True)
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.details_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.details_scroll.setWidgetResizable(True)
        self.details_scroll.setWidget(self.details_label)
        self.details_scroll.setMinimumWidth(280)
        self.details_scroll.setMaximumWidth(360)
        side.addWidget(self.details_scroll, 1)
        central = QWidget()
        layout = QHBoxLayout(central)
        left = QVBoxLayout()
        left.addWidget(self.view)
        left.addLayout(controls)
        layout.addLayout(left, 4)
        layout.addLayout(side, 1)
        self.setCentralWidget(central)
        self._update_interval(self.speed_slider.value())

    def _draw_graph(self) -> None:
        """Desenha conexões, zonas e rótulos estáticos."""
        for connection in self.graph.connections.values():
            first = self.graph.zones[connection.first]
            second = self.graph.zones[connection.second]
            x1, y1 = self.mapper.point(first.x, first.y)
            x2, y2 = self.mapper.point(second.x, second.y)
            self.scene.addItem(QGraphicsLineItem(x1, y1, x2, y2))
        for zone in self.graph.zones.values():
            x, y = self.mapper.point(zone.x, zone.y)
            item = QGraphicsEllipseItem(x - 24, y - 24, 48, 48)
            item.setBrush(QBrush(self._safe_color(zone.zone_type.value, zone.color)))
            item.setPen(QPen(QColor("white"), 2))
            self.scene.addItem(item)
            label = self.scene.addText(zone.name)
            label.setPos(x - 30, y + 28)
            self.zone_items[zone.name] = item
        self.scene.setSceneRect(self.scene.itemsBoundingRect().adjusted(-80, -80, 80, 80))

    def _create_drones(self) -> None:
        """Cria os círculos e identificadores dos drones."""
        identifiers = sorted(self.frames[0].positions)
        for identifier in identifiers:
            item = QGraphicsEllipseItem(-10, -10, 20, 20)
            item.setBrush(QBrush(QColor("#f5c542")))
            item.setPen(QPen(QColor("#222222"), 1))
            label = self.scene.addText(f"D{identifier}")
            self.scene.addItem(item)
            self.drone_items[identifier] = item
            self.drone_labels[identifier] = label

    def _apply_frame(self, frame: SimulationFrame) -> None:
        """Aplica posições e detalhes de um frame à cena."""
        self.frame_index = frame.turn
        self.turn_label.setText(f"Turno: {frame.turn}/{len(self.frames) - 1}")
        details = ["Movimentos:"]
        details.extend(f"  {movement}" for movement in frame.movements or ("nenhum",))
        for identifier, position in sorted(frame.positions.items()):
            details.append(f"D{identifier}: {position}")
            self._move_drone(identifier, position)
        if frame.zone_usage:
            details.append("Capacidades das zonas:")
            details.extend(
                f"  {name}: {used}/{limit or '∞'}"
                for name, (used, limit) in frame.zone_usage.items()
            )
        active_connections = [
            f"  {name}: {used}/{limit}"
            for name, (used, limit) in frame.connection_usage.items()
            if used
        ]
        if active_connections:
            details.append("Capacidades das conexões:")
            details.extend(active_connections)
        self.details_label.setText("\n".join(details))

    def _move_drone(self, identifier: int, position: str) -> None:
        """Move um drone para uma zona ou para o meio de uma conexão."""
        if position.startswith("@"):
            first, second = position[1:].split("-", 1)
            a = self.graph.zones[first]
            b = self.graph.zones[second]
            x = (a.x + b.x) / 2
            y = (a.y + b.y) / 2
        else:
            zone = self.graph.zones[position]
            x, y = zone.x, zone.y
        px, py = self.mapper.point(x, y)
        offset = (identifier % 3 - 1) * 14
        self.drone_items[identifier].setPos(px + offset, py + offset)
        self.drone_labels[identifier].setPos(px + 10 + offset, py - 12 + offset)

    def toggle_play(self) -> None:
        """Inicia ou pausa a reprodução automática."""
        if self.timer.isActive():
            self.timer.stop()
            self.play_button.setText("Play")
        else:
            if self.frame_index >= len(self.frames) - 1:
                self.reset()
            self.timer.start()
            self.play_button.setText("Pause")

    def next_frame(self) -> None:
        """Aplica o próximo frame, parando no fim."""
        if self.frame_index >= len(self.frames) - 1:
            self.timer.stop()
            self.play_button.setText("Play")
            return
        self._apply_frame(self.frames[self.frame_index + 1])

    def reset(self) -> None:
        """Retorna a interface ao frame inicial."""
        self.timer.stop()
        self.play_button.setText("Play")
        self._apply_frame(self.frames[0])

    def _update_interval(self, value: int) -> None:
        """Converte velocidade de 1-10 em intervalo do timer."""
        self.timer.setInterval(1100 - value * 100)

    @staticmethod
    def _zone_color(zone_type: str, color: str | None) -> str:
        """Escolhe cor informada ou cor semântica padrão."""
        if color:
            return color
        return {"blocked": "#666666", "restricted": "#e67e22", "priority": "#27ae60"}.get(
            zone_type, "#3498db"
        )

    @staticmethod
    def _safe_color(zone_type: str, color: str | None) -> QColor:
        """Converte uma cor do mapa e usa fallback se ela for inválida."""
        selected = QColor(SimulationWindow._zone_color(zone_type, color))
        if selected.isValid():
            return selected
        fallback = SimulationWindow._zone_color(zone_type, None)
        return QColor(fallback)
