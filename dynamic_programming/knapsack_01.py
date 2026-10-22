"""0/1 Knapsack for Loading Indivisible Urban Delivery Cargo.

Addresses logistics challenges where high-value items (servers, medical equipment, appliances)
cannot be partitioned. Implements:
1. Standard 2D Dynamic Programming table with backtracking for item reconstruction.
2. Space-optimized 1D rolling array reducing auxiliary memory from O(n * W) to O(W).
3. Pure recursive brute-force baseline exhibiting O(2^n) exponential blow-up.
4. Detailed hand-trace generation for report documentation.
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any
import time
import sys


@dataclass
class IndivisibleItem:
    """Represents an indivisible cargo item."""
    item_id: str
    name: str
    weight: int   # Integer weight for standard knapsack DP
    value: int    # Economic value / delivery priority score

    def __repr__(self) -> str:
        return f"Item({self.item_id}: '{self.name}', wt={self.weight}kg, val=${self.value})"


def knapsack_01_2d(
    items: List[IndivisibleItem],
    capacity: int
) -> Tuple[int, List[IndivisibleItem], List[List[int]], Dict[str, Any]]:
    """2D Bottom-Up Dynamic Programming for 0/1 Knapsack.

    Recurrence:
    dp[i][w] = dp[i-1][w]                                    if weight[i-1] > w
             = max(dp[i-1][w], value[i-1] + dp[i-1][w - weight[i-1]])  otherwise

    Time Complexity: O(n * W)
    Space Complexity: O(n * W)
    """
    n = len(items)
    # Initialize table (n+1) x (capacity+1)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = items[i - 1]
        wt = item.weight
        val = item.value
        for w in range(capacity + 1):
            if wt <= w:
                dp[i][w] = max(dp[i - 1][w], val + dp[i - 1][w - wt])
            else:
                dp[i][w] = dp[i - 1][w]

    max_value = dp[n][capacity]

    # Backtracking to reconstruct optimal subset of chosen items
    chosen_items: List[IndivisibleItem] = []
    w_curr = capacity
    for i in range(n, 0, -1):
        if dp[i][w_curr] != dp[i - 1][w_curr]:
            # Item i-1 was included
            item = items[i - 1]
            chosen_items.append(item)
            w_curr -= item.weight

    chosen_items.reverse()
    total_weight = sum(it.weight for it in chosen_items)

    stats = {
        "algorithm": "0/1 Knapsack 2D DP",
        "table_cells": (n + 1) * (capacity + 1),
        "total_value": max_value,
        "total_weight": total_weight,
        "capacity": capacity,
        "utilization_pct": round((total_weight / capacity) * 100.0, 1) if capacity > 0 else 0.0,
        "memory_bytes": sys.getsizeof(dp) + sum(sys.getsizeof(row) for row in dp)
    }

    return max_value, chosen_items, dp, stats


def knapsack_01_1d(
    items: List[IndivisibleItem],
    capacity: int
) -> Tuple[int, Dict[str, Any]]:
    """Space-Optimized 1D Rolling Array Dynamic Programming.

    Iterates backwards from capacity W down to item.weight to ensure each item
    is used at most once (avoiding unbounded knapsack behavior).

    Time Complexity: O(n * W)
    Space Complexity: O(W)  -- significant reduction from O(n * W)
    """
    dp = [0] * (capacity + 1)

    for item in items:
        wt = item.weight
        val = item.value
        # Iterate backwards to preserve values from previous step
        for w in range(capacity, wt - 1, -1):
            if dp[w - wt] + val > dp[w]:
                dp[w] = dp[w - wt] + val

    max_value = dp[capacity]

    stats = {
        "algorithm": "0/1 Knapsack 1D Optimized DP",
        "array_size": capacity + 1,
        "total_value": max_value,
        "capacity": capacity,
        "memory_bytes": sys.getsizeof(dp)
    }

    return max_value, stats


def knapsack_01_brute_force(
    items: List[IndivisibleItem],
    capacity: int
) -> Tuple[int, int, float]:
    """Pure recursive Brute-Force implementation exhibiting O(2^n) complexity.

    Used strictly for benchmarking and illustrating exponential explosion.
    Returns (max_value, recursive_call_count, elapsed_time_seconds).
    """
    call_count = 0

    def _recurse(idx: int, remaining_cap: int) -> int:
        nonlocal call_count
        call_count += 1

        if idx < 0 or remaining_cap <= 0:
            return 0

        item = items[idx]

        # Case 1: Exclude item
        without_item = _recurse(idx - 1, remaining_cap)

        # Case 2: Include item (if fits)
        with_item = 0
        if item.weight <= remaining_cap:
            with_item = item.value + _recurse(idx - 1, remaining_cap - item.weight)

        return max(without_item, with_item)

    t0 = time.perf_counter()
    max_val = _recurse(len(items) - 1, capacity)
    elapsed = time.perf_counter() - t0

    return max_val, call_count, elapsed


def compare_knapsack_implementations(
    items: List[IndivisibleItem],
    capacity: int
) -> Dict[str, Any]:
    """Benchmarks 2D DP, 1D DP, and Recursive Brute-Force to document performance differences."""
    # 1. 2D DP
    t0 = time.perf_counter()
    val_2d, chosen, _, stats_2d = knapsack_01_2d(items, capacity)
    t_2d = time.perf_counter() - t0

    # 2. 1D DP
    t0 = time.perf_counter()
    val_1d, stats_1d = knapsack_01_1d(items, capacity)
    t_1d = time.perf_counter() - t0

    # 3. Brute Force (only if n <= 25 to avoid freeze)
    n = len(items)
    if n <= 25:
        val_bf, bf_calls, t_bf = knapsack_01_brute_force(items, capacity)
    else:
        val_bf, bf_calls, t_bf = "Skipped (n > 25)", f"> 2^{n}", "N/A"

    memory_reduction_pct = (
        (1.0 - (stats_1d["memory_bytes"] / stats_2d["memory_bytes"])) * 100.0
        if stats_2d["memory_bytes"] > 0 else 0.0
    )

    return {
        "item_count_n": n,
        "capacity_W": capacity,
        "max_value_2d": val_2d,
        "max_value_1d": val_1d,
        "max_value_bf": val_bf,
        "runtime_2d_ms": round(t_2d * 1000.0, 4),
        "runtime_1d_ms": round(t_1d * 1000.0, 4),
        "runtime_bf_ms": round(t_bf * 1000.0, 4) if isinstance(t_bf, (int, float)) else t_bf,
        "bf_recursive_calls": bf_calls,
        "memory_2d_bytes": stats_2d["memory_bytes"],
        "memory_1d_bytes": stats_1d["memory_bytes"],
        "memory_reduction_pct": round(memory_reduction_pct, 2),
        "chosen_items": chosen
    }


def trace_knapsack_table(items: List[IndivisibleItem], capacity: int) -> Tuple[List[str], List[List[int]]]:
    """Generates hand-traceable table headers and 2D matrix for the report."""
    _, _, dp, _ = knapsack_01_2d(items, capacity)
    headers = [f"W={w}" for w in range(capacity + 1)]
    return headers, dp
