"""Merge Sort implementation for Warehouse Queue Dispatch.

This module sorts packages based on delivery deadline and priority.
It is instrumented to measure comparisons and empirically verify O(n log n) complexity.
"""

from dataclasses import dataclass
from typing import List, Tuple, Callable, Any, Optional
import math


@dataclass
class Package:
    """Represents a delivery package in the warehouse queue."""
    package_id: str
    recipient: str
    deadline_hour: float  # Delivery deadline in hours from warehouse open (e.g. 9.5 = 9:30 AM)
    priority: int         # 1 = Standard, 2 = Express, 3 = Urgent / Critical
    weight_kg: float
    destination_zone: str

    def __repr__(self) -> str:
        return (f"Package({self.package_id}, deadline={self.deadline_hour}h, "
                f"prio={self.priority}, {self.weight_kg}kg, {self.destination_zone})")


def package_comparator(a: Package, b: Package) -> int:
    """Default comparator: Sort by earliest deadline ascending; tie-break by priority descending."""
    if a.deadline_hour < b.deadline_hour:
        return -1
    elif a.deadline_hour > b.deadline_hour:
        return 1
    else:
        # Tie-breaker: higher priority first
        if a.priority > b.priority:
            return -1
        elif a.priority < b.priority:
            return 1
        return 0


def merge_sort_packages(
    packages: List[Package],
    key: Optional[Callable[[Package], Any]] = None,
    reverse: bool = False
) -> List[Package]:
    """Genuinely recursive Merge Sort for sorting package lists.

    Handles edge cases: empty list, single element, duplicates.
    Time Complexity: O(n log n) in all cases (best, worst, average).
    Space Complexity: O(n) auxiliary space.
    """
    if len(packages) <= 1:
        return list(packages)

    mid = len(packages) // 2
    left_half = merge_sort_packages(packages[:mid], key=key, reverse=reverse)
    right_half = merge_sort_packages(packages[mid:], key=key, reverse=reverse)

    return _merge(left_half, right_half, key=key, reverse=reverse)


def _merge(
    left: List[Package],
    right: List[Package],
    key: Optional[Callable[[Package], Any]] = None,
    reverse: bool = False
) -> List[Package]:
    """Merges two sorted lists into a single sorted list."""
    merged: List[Package] = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if key is not None:
            val_l = key(left[i])
            val_r = key(right[j])
            condition = (val_l > val_r) if reverse else (val_l <= val_r)
        else:
            comp = package_comparator(left[i], right[j])
            condition = (comp >= 0) if reverse else (comp <= 0)

        if condition:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


class MergeSortInstrumented:
    """Instrumented version of recursive Merge Sort to count comparisons and track recursion depth."""

    def __init__(self):
        self.comparison_count = 0
        self.recursive_calls = 0
        self.max_recursion_depth = 0

    def sort(
        self,
        items: List[Any],
        key: Optional[Callable[[Any], Any]] = None,
        _depth: int = 1
    ) -> List[Any]:
        """Recursive sort with instrumentation tracking."""
        self.recursive_calls += 1
        if _depth > self.max_recursion_depth:
            self.max_recursion_depth = _depth

        n = len(items)
        if n <= 1:
            return list(items)

        mid = n // 2
        left = self.sort(items[:mid], key=key, _depth=_depth + 1)
        right = self.sort(items[mid:], key=key, _depth=_depth + 1)

        return self._merge_instrumented(left, right, key=key)

    def _merge_instrumented(
        self,
        left: List[Any],
        right: List[Any],
        key: Optional[Callable[[Any], Any]] = None
    ) -> List[Any]:
        merged = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):
            self.comparison_count += 1
            val_l = key(left[i]) if key else left[i]
            val_r = key(right[j]) if key else right[j]

            if val_l <= val_r:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged


def merge_sort_instrumented(
    items: List[Any],
    key: Optional[Callable[[Any], Any]] = None
) -> Tuple[List[Any], int, int, int]:
    """Sorts items and returns (sorted_list, comparisons, recursive_calls, max_depth)."""
    instrumenter = MergeSortInstrumented()
    sorted_items = instrumenter.sort(items, key=key)
    return (
        sorted_items,
        instrumenter.comparison_count,
        instrumenter.recursive_calls,
        instrumenter.max_recursion_depth,
    )


def benchmark_merge_sort_complexity(sizes: List[int]) -> List[dict]:
    """Runs merge sort across varying input sizes to empirically verify O(n log n).

    Returns a table comparing actual comparisons against theoretical n * log2(n).
    """
    import random
    results = []
    for n in sizes:
        # Generate random package deadlines
        sample = [random.uniform(1.0, 100.0) for _ in range(n)]
        _, comps, calls, depth = merge_sort_instrumented(sample)

        theoretical_nlogn = n * math.log2(n) if n > 0 else 0
        ratio = comps / theoretical_nlogn if theoretical_nlogn > 0 else 0

        results.append({
            "n": n,
            "comparisons": comps,
            "n_log2_n": round(theoretical_nlogn, 2),
            "ratio (comps / n_log_n)": round(ratio, 4),
            "recursive_calls": calls,
            "max_depth": depth,
            "theoretical_depth": math.ceil(math.log2(n)) + 1 if n > 0 else 1
        })
    return results
