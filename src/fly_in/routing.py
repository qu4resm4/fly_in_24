"""Planejamento de rotas com busca de menor custo."""

from __future__ import annotations

import heapq
from dataclasses import dataclass
from math import ceil

from .models import Graph, ZoneType


class NoRouteError(RuntimeError):
    """Indica que não existe uma rota acessível."""


@dataclass(frozen=True)
class RouteMetrics:
    """Métricas estáticas usadas para comparar rotas candidatas."""

    cost: int
    throughput: int
    priority_penalty: int

    @property
    def bottleneck_penalty(self) -> int:
        """Retorna uma penalidade pequena para rotas de baixa vazão."""
        return max(0, 4 - self.throughput)


class RoutePlanner:
    """Encontra rotas ponderadas em um grafo Fly-in."""

    def __init__(self, graph: Graph) -> None:
        self.graph = graph

    def shortest_path(self, start: str, goal: str) -> list[str]:
        """Retorna a rota de menor custo, preferindo zonas priority em empates."""
        queue: list[tuple[int, int, str, tuple[str, ...]]] = [(0, 0, start, (start,))]
        best: dict[str, tuple[int, int]] = {start: (0, 0)}
        while queue:
            cost, hops, current, path = heapq.heappop(queue)
            if current == goal:
                return list(path)
            if (cost, hops) != best.get(current):
                continue
            for neighbor in self.graph.adjacency[current]:
                zone = self.graph.zones[neighbor]
                if not zone.accessible:
                    continue
                priority_bonus = 0 if zone.zone_type is ZoneType.PRIORITY else 1
                candidate = (cost + zone.zone_type.movement_cost, hops + priority_bonus)
                if candidate < best.get(neighbor, (10**9, 10**9)):
                    best[neighbor] = candidate
                    heapq.heappush(
                        queue, (candidate[0], candidate[1], neighbor, path + (neighbor,))
                    )
        raise NoRouteError(f"não existe rota entre {start} e {goal}")

    def plan_routes(self, start: str, goal: str, drone_count: int) -> list[list[str]]:
        """Distribui drones entre rotas pelo custo e pela vazão prevista."""
        candidates: list[tuple[RouteMetrics, list[str]]] = []

        def visit(current: str, path: list[str]) -> None:
            if len(candidates) >= 32 and current != goal:
                return
            if current == goal:
                metrics = self._metrics(path)
                candidates.append((metrics, path.copy()))
                return
            for neighbor in self.graph.adjacency[current]:
                if neighbor in path or not self.graph.zones[neighbor].accessible:
                    continue
                visit(neighbor, path + [neighbor])

        visit(start, [start])
        if not candidates:
            raise NoRouteError(f"não existe rota entre {start} e {goal}")
        candidates.sort(key=lambda item: (item[0].cost, item[0].priority_penalty, len(item[1])))
        # Mantém a busca limitada, mas inclui rotas ligeiramente mais longas
        # para que uma rota com maior vazão possa vencer um gargalo.
        best_cost = candidates[0][0].cost
        candidates = [item for item in candidates if item[0].cost <= best_cost + 3][:32]
        assigned = [0] * len(candidates)
        routes: list[list[str]] = []
        for _ in range(drone_count):
            choice = min(
                range(len(candidates)),
                key=lambda index: self._estimated_completion(candidates[index][0], assigned[index]),
            )
            assigned[choice] += 1
            routes.append(candidates[choice][1].copy())
        return routes

    def _metrics(self, path: list[str]) -> RouteMetrics:
        """Calcula custo e vazão mínima de uma rota."""
        cost = sum(self.graph.zones[name].zone_type.movement_cost for name in path[1:])
        priority_penalty = sum(
            self.graph.zones[name].zone_type is not ZoneType.PRIORITY for name in path[1:]
        )
        capacities: list[int] = []
        for name in path[1:-1]:
            capacities.append(self.graph.zones[name].capacity)
        for first, second in zip(path, path[1:]):
            capacities.append(self.graph.connection_between(first, second).capacity)
        return RouteMetrics(cost, min(capacities, default=1), priority_penalty)

    @staticmethod
    def _estimated_completion(metrics: RouteMetrics, assigned: int) -> tuple[int, int, int, int]:
        """Estima o turno de conclusão do próximo drone da rota."""
        completion = metrics.cost + ceil((assigned + 1) / metrics.throughput) - 1
        return (completion, metrics.bottleneck_penalty, metrics.priority_penalty, assigned)
