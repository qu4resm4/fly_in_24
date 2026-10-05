"""Modelos de domínio do simulador Fly-in."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class ZoneType(str, Enum):
    """Tipos de zona suportados pelo formato Fly-in."""

    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    @property
    def movement_cost(self) -> int:
        """Retorna o custo em turnos para chegar à zona."""
        return 2 if self is ZoneType.RESTRICTED else 1


@dataclass
class Zone:
    """Representa uma zona do mapa."""

    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    capacity: int = 1
    is_start: bool = False
    is_end: bool = False

    @property
    def accessible(self) -> bool:
        """Indica se drones podem entrar na zona."""
        return self.zone_type is not ZoneType.BLOCKED


@dataclass(frozen=True)
class Connection:
    """Representa uma conexão bidirecional entre duas zonas."""

    first: str
    second: str
    capacity: int = 1

    def key(self) -> frozenset[str]:
        """Retorna uma chave independente da direção da conexão."""
        return frozenset((self.first, self.second))

    def label_from(self, source: str) -> str:
        """Retorna a representação textual da conexão a partir de uma zona."""
        if source == self.first:
            return f"{self.first}-{self.second}"
        return f"{self.second}-{self.first}"


@dataclass
class Drone:
    """Estado mutável de um drone durante a simulação."""

    identifier: int
    route: list[str]
    route_index: int = 0
    location: str = ""
    transit_destination: str | None = None
    transit_connection: str | None = None
    transit_remaining: int = 0

    @property
    def delivered(self) -> bool:
        """Indica se o drone chegou ao destino."""
        return self.transit_destination is None and self.route_index >= len(self.route) - 1


@dataclass
class Graph:
    """Grafo não direcionado construído sem biblioteca externa."""

    zones: dict[str, Zone] = field(default_factory=dict)
    connections: dict[frozenset[str], Connection] = field(default_factory=dict)
    adjacency: dict[str, list[str]] = field(default_factory=dict)

    def add_zone(self, zone: Zone) -> None:
        """Adiciona uma zona única ao grafo."""
        if zone.name in self.zones:
            raise ValueError(f"zona duplicada: {zone.name}")
        self.zones[zone.name] = zone
        self.adjacency[zone.name] = []

    def add_connection(self, connection: Connection) -> None:
        """Adiciona uma conexão bidirecional entre zonas existentes."""
        if connection.first not in self.zones or connection.second not in self.zones:
            raise ValueError("conexão referencia uma zona inexistente")
        if connection.key() in self.connections:
            raise ValueError("conexão duplicada")
        self.connections[connection.key()] = connection
        self.adjacency[connection.first].append(connection.second)
        self.adjacency[connection.second].append(connection.first)

    def connection_between(self, first: str, second: str) -> Connection:
        """Retorna a conexão entre duas zonas."""
        return self.connections[frozenset((first, second))]
