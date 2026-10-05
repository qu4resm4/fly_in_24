"""Formatadores de saída oficial e visual."""

from __future__ import annotations

from .models import Graph
from .simulation import Turn


class OutputFormatter:
    """Produz a saída compatível com a avaliação."""

    @staticmethod
    def official(turns: list[Turn]) -> str:
        """Retorna um turno por linha, sem informação decorativa."""
        return "\n".join(" ".join(turn.movements) for turn in turns)


class TerminalVisualizer:
    """Produz uma visualização textual opcional da simulação."""

    _colors = {"red": 31, "green": 32, "yellow": 33, "blue": 34, "purple": 35,
               "cyan": 36, "gray": 90, "orange": 33, "gold": 33}

    def render(self, graph: Graph, turns: list[Turn], show_capacity: bool = False) -> str:
        """Renderiza turnos, movimentos e capacidades em texto ANSI."""
        lines: list[str] = []
        for index, turn in enumerate(turns, 1):
            lines.append(f"Turn {index}")
            lines.append(self._map_line(graph, index, turns))
            lines.append("Movimentos: " + (" ".join(turn.movements) or "nenhum"))
            if show_capacity:
                zones = " ".join(
                    f"{name}={used}/{limit or '∞'}"
                    for name, (used, limit) in turn.zone_usage.items()
                )
                lines.append("Zonas: " + zones)
                connections = " ".join(
                    f"{name}={used}/{limit}"
                    for name, (used, limit) in turn.connection_usage.items()
                    if used
                )
                lines.append("Conexões: " + (connections or "nenhuma"))
            lines.append("")
        return "\n".join(lines).rstrip()

    def _map_line(self, graph: Graph, _index: int, turns: list[Turn]) -> str:
        """Renderiza uma linha compacta com as zonas e drones atuais."""
        last_turn = turns[_index - 1]
        movements = " ".join(last_turn.movements)
        zones = []
        for zone in graph.zones.values():
            color = self._colors.get(zone.color or "", 0)
            label = f"{zone.name}"
            if color:
                label = f"\033[{color}m{label}\033[0m"
            zones.append(label)
        return "Mapa: " + " - ".join(zones) + (f" | {movements}" if movements else "")
