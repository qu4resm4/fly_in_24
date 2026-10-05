"""Contrato entre a simulação e as interfaces de apresentação."""

from __future__ import annotations

from dataclasses import dataclass

from ..models import Graph
from ..simulation import Turn


@dataclass(frozen=True)
class SimulationFrame:
    """Estado imutável da simulação em um turno visualizável."""

    turn: int
    positions: dict[int, str]
    movements: tuple[str, ...]
    zone_usage: dict[str, tuple[int, int]]
    connection_usage: dict[str, tuple[int, int]]


def create_frames(graph: Graph, start: str, drone_count: int,
                  turns: list[Turn]) -> list[SimulationFrame]:
    """Cria um frame inicial e um frame para cada turno executado."""
    initial_positions = {identifier: start for identifier in range(1, drone_count + 1)}
    frames = [_frame(0, initial_positions, (), graph, {}, {})]
    for turn_number, turn in enumerate(turns, 1):
        frames.append(
            _frame(turn_number, turn.positions, tuple(turn.movements), graph,
                   turn.zone_usage, turn.connection_usage)
        )
    return frames


def _frame(turn: int, positions: dict[int, str], movements: tuple[str, ...],
           graph: Graph, zone_usage: dict[str, tuple[int, int]],
           connection_usage: dict[str, tuple[int, int]]) -> SimulationFrame:
    """Copia os dados mutáveis de um turno para um frame seguro."""
    del graph  # Mantém a assinatura preparada para validações futuras do mapa.
    return SimulationFrame(
        turn, dict(positions), movements, dict(zone_usage), dict(connection_usage)
    )
