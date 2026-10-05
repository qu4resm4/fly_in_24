"""Parser e validação dos arquivos de mapa Fly-in."""

from __future__ import annotations

import re
from pathlib import Path

from .models import Connection, Graph, Zone, ZoneType


class MapParseError(ValueError):
    """Erro de sintaxe ou validação em um mapa."""


class MapParser:
    """Converte um arquivo Fly-in em um grafo validado."""

    _zone_pattern = re.compile(
        r"^(start_hub|end_hub|hub):\s+(\S+)\s+(-?\d+)\s+(-?\d+)"
        r"(?:\s+\[(.*)\])?$"
    )
    _connection_pattern = re.compile(r"^connection:\s+(\S+)-(\S+)(?:\s+\[(.*)\])?$")

    def parse(self, path: str | Path) -> tuple[int, Graph, str, str]:
        """Lê e valida um arquivo, retornando drones, grafo, início e fim."""
        graph = Graph()
        drone_count: int | None = None
        start_name: str | None = None
        end_name: str | None = None
        pending_connections: list[tuple[int, str, str, int]] = []

        try:
            with Path(path).open(encoding="utf-8") as file:
                lines = list(file)
        except OSError as error:
            raise MapParseError(f"não foi possível abrir o mapa: {error}") from error

        for line_number, raw_line in enumerate(lines, start=1):
            line = raw_line.split("#", 1)[0].strip()
            if not line:
                continue
            try:
                if line.startswith("nb_drones:"):
                    if drone_count is not None:
                        raise ValueError("nb_drones duplicado")
                    drone_count = self._positive_int(line.split(":", 1)[1].strip(), "nb_drones")
                    continue
                zone_match = self._zone_pattern.match(line)
                if zone_match:
                    kind, name, x_text, y_text, metadata_text = zone_match.groups()
                    metadata = self._metadata(metadata_text)
                    zone_type = self._zone_type(metadata.get("zone", "normal"))
                    capacity = self._positive_int(metadata.get("max_drones", "1"), "max_drones")
                    zone = Zone(
                        name, int(x_text), int(y_text), zone_type, metadata.get("color"), capacity,
                        kind == "start_hub", kind == "end_hub"
                    )
                    graph.add_zone(zone)
                    if kind == "start_hub":
                        if start_name is not None:
                            raise ValueError("start_hub duplicado")
                        start_name = name
                    if kind == "end_hub":
                        if end_name is not None:
                            raise ValueError("end_hub duplicado")
                        end_name = name
                    continue
                connection_match = self._connection_pattern.match(line)
                if connection_match:
                    first, second, metadata_text = connection_match.groups()
                    metadata = self._metadata(metadata_text)
                    capacity = self._positive_int(metadata.get("max_link_capacity", "1"),
                                                  "max_link_capacity")
                    pending_connections.append((line_number, first, second, capacity))
                    continue
                raise ValueError("formato desconhecido")
            except (TypeError, ValueError) as error:
                raise MapParseError(f"linha {line_number}: {error}") from error

        if drone_count is None:
            raise MapParseError("mapa não define nb_drones")
        if start_name is None:
            raise MapParseError("mapa não define start_hub")
        if end_name is None:
            raise MapParseError("mapa não define end_hub")
        for line_number, first, second, capacity in pending_connections:
            try:
                graph.add_connection(Connection(first, second, capacity))
            except ValueError as error:
                raise MapParseError(f"linha {line_number}: {error}") from error
        return drone_count, graph, start_name, end_name

    @staticmethod
    def _metadata(text: str | None) -> dict[str, str]:
        """Interpreta os pares chave=valor do bloco opcional."""
        if text is None or not text.strip():
            return {}
        metadata: dict[str, str] = {}
        for item in text.split():
            if "=" not in item:
                raise ValueError(f"metadado inválido: {item}")
            key, value = item.split("=", 1)
            if not key or not value or key in metadata:
                raise ValueError(f"metadado inválido: {item}")
            metadata[key] = value
        return metadata

    @staticmethod
    def _positive_int(value: str, field: str) -> int:
        """Valida um inteiro positivo."""
        try:
            number = int(value)
        except ValueError as error:
            raise ValueError(f"{field} deve ser inteiro positivo") from error
        if number <= 0:
            raise ValueError(f"{field} deve ser inteiro positivo")
        return number

    @staticmethod
    def _zone_type(value: str) -> ZoneType:
        """Converte o texto do tipo de zona para o enum de domínio."""
        try:
            return ZoneType(value)
        except ValueError as error:
            raise ValueError(f"tipo de zona inválido: {value}") from error
