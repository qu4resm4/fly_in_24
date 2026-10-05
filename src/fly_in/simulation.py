"""Motor de simulação discreta para os drones."""

from __future__ import annotations

from dataclasses import dataclass, field

from .models import Drone, Graph, ZoneType


@dataclass
class Turn:
    """Movimentos e ocupações observados em um turno."""

    movements: list[str] = field(default_factory=list)
    zone_usage: dict[str, tuple[int, int]] = field(default_factory=dict)
    connection_usage: dict[str, tuple[int, int]] = field(default_factory=dict)
    positions: dict[int, str] = field(default_factory=dict)


class SimulationError(RuntimeError):
    """Erro de execução da simulação."""


class Simulation:
    """Executa rotas atribuídas respeitando capacidades por turno."""

    def __init__(self, graph: Graph, start: str, goal: str, routes: list[list[str]]) -> None:
        self.graph = graph
        self.start = start
        self.goal = goal
        self.drones = [Drone(index, route, location=start) for index, route in enumerate(routes, 1)]

    def run(self, max_turns: int = 10000) -> list[Turn]:
        """Executa a simulação até entregar todos os drones."""
        turns: list[Turn] = []
        for _ in range(max_turns):
            if all(drone.delivered for drone in self.drones):
                return turns
            turn = self._advance_turn()
            if not turn.movements and not all(drone.delivered for drone in self.drones):
                raise SimulationError("simulação bloqueada: nenhum drone pode avançar")
            turns.append(turn)
        raise SimulationError("limite de turnos excedido")

    def _advance_turn(self) -> Turn:
        """Planeja e aplica um único turno."""
        turn = Turn()
        outgoing: dict[str, int] = {}
        incoming: dict[str, int] = {}
        connection_usage: dict[frozenset[str], int] = {}
        for drone in self.drones:
            if drone.delivered:
                continue
            if drone.transit_destination is not None:
                drone.transit_remaining -= 1
                if drone.transit_remaining == 0:
                    destination = drone.transit_destination
                    drone.transit_destination = None
                    drone.transit_connection = None
                    drone.location = destination
                    drone.route_index += 1
                    turn.movements.append(f"D{drone.identifier}-{destination}")
                continue
            if drone.route_index >= len(drone.route) - 1:
                continue
            source = drone.route[drone.route_index]
            destination = drone.route[drone.route_index + 1]
            connection = self.graph.connection_between(source, destination)
            key = connection.key()
            used = connection_usage.get(key, 0)
            if used >= connection.capacity:
                continue
            destination_zone = self.graph.zones[destination]
            current_occupancy = sum(1 for item in self.drones if item.location == destination)
            free_after_exit = outgoing.get(destination, 0)
            reserved = incoming.get(destination, 0)
            if (
                not destination_zone.is_end
                and current_occupancy - free_after_exit + reserved >= destination_zone.capacity
            ):
                continue
            outgoing[source] = outgoing.get(source, 0) + 1
            incoming[destination] = reserved + 1
            connection_usage[key] = used + 1
            label = connection.label_from(source)
            if destination_zone.zone_type is ZoneType.RESTRICTED:
                drone.transit_destination = destination
                drone.transit_connection = label
                drone.transit_remaining = 1
                turn.movements.append(f"D{drone.identifier}-{label}")
            else:
                drone.location = destination
                drone.route_index += 1
                turn.movements.append(f"D{drone.identifier}-{destination}")
        turn.zone_usage = self._zone_usage()
        turn.connection_usage = self._connection_usage(connection_usage)
        turn.positions = self._drone_positions()
        return turn

    def _drone_positions(self) -> dict[int, str]:
        """Retorna posições legíveis, incluindo drones em trânsito."""
        positions: dict[int, str] = {}
        for drone in self.drones:
            if drone.transit_destination is not None and drone.transit_connection is not None:
                positions[drone.identifier] = f"@{drone.transit_connection}"
            else:
                positions[drone.identifier] = drone.location
        return positions

    def _zone_usage(self) -> dict[str, tuple[int, int]]:
        """Calcula ocupação atual das zonas."""
        usage: dict[str, tuple[int, int]] = {}
        for name, zone in self.graph.zones.items():
            count = sum(
                1 for drone in self.drones
                if drone.location == name and drone.transit_destination is None
            )
            limit = 0 if zone.is_start or zone.is_end else zone.capacity
            usage[name] = (count, limit)
        return usage

    def _connection_usage(self, usage: dict[frozenset[str], int]) -> dict[str, tuple[int, int]]:
        """Converte o uso das conexões para labels legíveis."""
        result: dict[str, tuple[int, int]] = {}
        for key, connection in self.graph.connections.items():
            label = f"{connection.first}-{connection.second}"
            result[label] = (usage.get(key, 0), connection.capacity)
        return result
