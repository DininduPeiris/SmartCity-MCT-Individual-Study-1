"""Bellman-Ford Dynamic Programming Algorithm for City Delivery Routing.

Models the metropolitan road network as a directed weighted graph where vertices
represent logistics hubs or delivery drop-off points, and edge weights represent transit
times (in minutes) or operational costs (accounting for fuel, tolls, and congestion).
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Any


@dataclass(frozen=True)
class CityEdge:
    """Represents a road/corridor link between two city nodes."""
    source: str
    target: str
    weight: float   # Transit cost / travel time in minutes
    road_name: str = ""

    def __repr__(self) -> str:
        name_str = f" ({self.road_name})" if self.road_name else ""
        return f"{self.source} -> {self.target} [{self.weight:.1f}m{name_str}]"


class CityGraph:
    """Directed weighted graph representing urban road network."""

    def __init__(self):
        self.vertices: set[str] = set()
        self.edges: List[CityEdge] = []
        self.adjacency: Dict[str, List[Tuple[str, float]]] = {}

    def add_vertex(self, vertex: str):
        self.vertices.add(vertex)
        if vertex not in self.adjacency:
            self.adjacency[vertex] = []

    def add_edge(self, source: str, target: str, weight: float, road_name: str = ""):
        self.add_vertex(source)
        self.add_vertex(target)
        edge = CityEdge(source=source, target=target, weight=weight, road_name=road_name)
        self.edges.append(edge)
        self.adjacency[source].append((target, weight))


def bellman_ford_dp(
    graph: CityGraph,
    source_vertex: str
) -> Tuple[Dict[str, float], Dict[str, Optional[str]], bool, Dict[str, Any]]:
    """Bellman-Ford Dynamic Programming Algorithm.

    DP Formulation:
    Let dp[k][v] be the minimum cost from source to vertex v using at most k edges.
    dp[0][source] = 0, dp[0][v] = infinity for v != source.
    dp[k][v] = min( dp[k-1][v], min_{(u,v) in E} (dp[k-1][u] + weight(u,v)) )

    Time Complexity: O(|V| * |E|)
    Space Complexity: O(|V|)
    """
    if source_vertex not in graph.vertices:
        raise ValueError(f"Source vertex '{source_vertex}' does not exist in graph.")

    vertices = list(graph.vertices)
    num_vertices = len(vertices)

    # Initialize distance and predecessor tables
    distance: Dict[str, float] = {v: float("inf") for v in vertices}
    predecessor: Dict[str, Optional[str]] = {v: None for v in vertices}
    distance[source_vertex] = 0.0

    iteration_history: List[Dict[str, float]] = [dict(distance)]

    # Dynamic Programming: Relax all edges |V| - 1 times
    for k in range(1, num_vertices):
        updated = False
        # Create a copy to prevent using newly updated values in same step (pure DP semantics)
        prev_distance = dict(distance)

        for edge in graph.edges:
            u, v, w = edge.source, edge.target, edge.weight
            if prev_distance[u] != float("inf") and prev_distance[u] + w < distance[v]:
                distance[v] = round(prev_distance[u] + w, 3)
                predecessor[v] = u
                updated = True

        iteration_history.append(dict(distance))

        # Early termination if no relaxation occurred
        if not updated:
            break

    # Check for negative-weight cycles
    has_negative_cycle = False
    for edge in graph.edges:
        u, v, w = edge.source, edge.target, edge.weight
        if distance[u] != float("inf") and distance[u] + w < distance[v]:
            has_negative_cycle = True
            break

    stats = {
        "source": source_vertex,
        "vertex_count": num_vertices,
        "edge_count": len(graph.edges),
        "iterations_run": len(iteration_history) - 1,
        "max_possible_iterations": num_vertices - 1,
        "has_negative_cycle": has_negative_cycle,
        "reachable_destinations": sum(1 for d in distance.values() if d < float("inf")),
        "iteration_history": iteration_history
    }

    return distance, predecessor, has_negative_cycle, stats


def reconstruct_path(predecessor: Dict[str, Optional[str]], target: str) -> List[str]:
    """Reconstructs the sequence of nodes from source to target."""
    path = []
    curr: Optional[str] = target
    visited = set()

    while curr is not None:
        if curr in visited:
            # Cycle detected during reconstruction
            break
        visited.add(curr)
        path.append(curr)
        curr = predecessor.get(curr)

    path.reverse()
    return path
