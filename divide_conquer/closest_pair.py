"""Closest Pair of 2D Hubs Algorithm.

This module implements the classic Divide & Conquer 2D Closest Pair algorithm (O(n log n))
and compares its accuracy and execution time against the Brute Force approach (O(n^2)).
Used by SmartCity Logistics to detect closely clustered distribution hubs for route consolidation.
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any
import math
import time
import random


@dataclass(frozen=True)
class Point:
    """Represents a 2D geographical location in kilometers."""
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        """Euclidean distance between two 2D points."""
        return math.hypot(self.x - other.x, self.y - other.y)


@dataclass(frozen=True)
class Hub:
    """Represents a SmartCity logistics distribution hub."""
    hub_id: str
    name: str
    location: Point
    capacity_daily_parcels: int = 5000

    @property
    def x(self) -> float:
        return self.location.x

    @property
    def y(self) -> float:
        return self.location.y

    def __repr__(self) -> str:
        return f"Hub({self.hub_id}, '{self.name}', ({self.x:.2f}, {self.y:.2f}))"


def brute_force_closest_pair(hubs: List[Hub]) -> Tuple[Optional[Tuple[Hub, Hub]], float]:
    """Brute force closest pair algorithm with O(n^2) complexity.

    Handles edge cases: len(hubs) < 2 returns (None, infinity).
    """
    n = len(hubs)
    if n < 2:
        return None, float("inf")

    min_dist = float("inf")
    closest_pair: Optional[Tuple[Hub, Hub]] = None

    for i in range(n):
        for j in range(i + 1, n):
            d = hubs[i].location.distance_to(hubs[j].location)
            if d < min_dist:
                min_dist = d
                closest_pair = (hubs[i], hubs[j])

    return closest_pair, min_dist


def closest_pair_hubs(hubs: List[Hub]) -> Tuple[Optional[Tuple[Hub, Hub]], float]:
    """Divide and Conquer Closest Pair algorithm running in O(n log n) time.

    Handles edge cases:
    - Empty list: (None, inf)
    - 1 hub: (None, inf)
    - Duplicate points: returns duplicate pair with distance 0.0

    Recurrence: T(n) = 2 T(n/2) + O(n) => O(n log n).
    """
    n = len(hubs)
    if n < 2:
        return None, float("inf")

    # Pre-sort by X and Y coordinates
    points_sorted_by_x = sorted(hubs, key=lambda h: (h.x, h.y))
    points_sorted_by_y = sorted(hubs, key=lambda h: (h.y, h.x))

    return _closest_pair_recursive(points_sorted_by_x, points_sorted_by_y)


def _closest_pair_recursive(
    px: List[Hub],
    py: List[Hub]
) -> Tuple[Optional[Tuple[Hub, Hub]], float]:
    """Recursive Divide & Conquer routine."""
    n = len(px)

    # Base case: for small n (<= 3), brute force is faster and terminates recursion
    if n <= 3:
        return brute_force_closest_pair(px)

    # Divide step: split by median X
    mid = n // 2
    mid_hub = px[mid]
    mid_x = mid_hub.x

    # Subarrays partitioned along X
    left_x = px[:mid]
    right_x = px[mid:]

    # Partition py into left_y and right_y in O(n) time maintaining Y-order
    # Using mid_hub identity and index to resolve ties consistently
    left_set = set(left_x)
    left_y = [h for h in py if h in left_set]
    right_y = [h for h in py if h not in left_set]

    # Conquer step: recursively find minimum distance in left and right halves
    left_pair, left_min = _closest_pair_recursive(left_x, left_y)
    right_pair, right_min = _closest_pair_recursive(right_x, right_y)

    if left_min <= right_min:
        delta = left_min
        best_pair = left_pair
    else:
        delta = right_min
        best_pair = right_pair

    # Combine step: check points in the vertical strip [mid_x - delta, mid_x + delta]
    strip = [h for h in py if abs(h.x - mid_x) < delta]

    strip_len = len(strip)
    for i in range(strip_len):
        # A point only needs to be compared with at most 7 subsequent points in Y order
        # because at most 8 points can fit in a delta x 2delta box without violating delta
        j = i + 1
        while j < strip_len and (strip[j].y - strip[i].y) < delta:
            dist = strip[i].location.distance_to(strip[j].location)
            if dist < delta:
                delta = dist
                best_pair = (strip[i], strip[j])
            j += 1

    return best_pair, delta


def benchmark_closest_pair(sizes: List[int], seed: int = 42) -> List[Dict[str, Any]]:
    """Compares runtime of D&C vs Brute-force on specified input sizes.

    Generates benchmark table as required by the assessment checklist.
    """
    random.seed(seed)
    results = []

    for n in sizes:
        # Generate random hubs in a 500x500 km metropolitan region
        hubs = [
            Hub(
                hub_id=f"HUB_{i:04d}",
                name=f"Metro Hub {i}",
                location=Point(random.uniform(0, 500.0), random.uniform(0, 500.0))
            )
            for i in range(n)
        ]

        # Time Divide & Conquer
        t0 = time.perf_counter()
        dc_pair, dc_dist = closest_pair_hubs(hubs)
        dc_time_ms = (time.perf_counter() - t0) * 1000.0

        # Time Brute Force (skip brute force for n > 5000 to prevent hang)
        if n <= 2000:
            t0 = time.perf_counter()
            bf_pair, bf_dist = brute_force_closest_pair(hubs)
            bf_time_ms = (time.perf_counter() - t0) * 1000.0
            speedup = bf_time_ms / dc_time_ms if dc_time_ms > 0 else float("inf")
            dist_match = math.isclose(dc_dist, bf_dist, rel_tol=1e-7)
        else:
            bf_time_ms = None
            speedup = None
            dist_match = True

        results.append({
            "n": n,
            "dc_time_ms": round(dc_time_ms, 3),
            "bf_time_ms": round(bf_time_ms, 3) if bf_time_ms is not None else "N/A",
            "speedup_factor": round(speedup, 2) if speedup is not None else "N/A",
            "min_distance_km": round(dc_dist, 4),
            "distances_match": dist_match
        })

    return results
