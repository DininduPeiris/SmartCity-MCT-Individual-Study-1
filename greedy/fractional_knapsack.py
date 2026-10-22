"""Fractional Knapsack for Loading Urban Delivery Vans with Divisible Cargo.

Used for bulk materials, fluids, parcel aggregates, and granular supplies where partial
quantities can be loaded to maximize total inventory value within van payload limits.
"""

from dataclasses import dataclass
from typing import List, Tuple, Dict, Any


@dataclass
class CargoItem:
    """Represents divisible cargo to be loaded onto a delivery van."""
    item_id: str
    name: str
    weight: float   # in kg
    value: float    # in USD / economic value metric

    @property
    def value_per_kg(self) -> float:
        return self.value / self.weight if self.weight > 0 else 0.0

    def __repr__(self) -> str:
        return f"CargoItem({self.item_id}, '{self.name}', wt={self.weight}kg, val=${self.value}, ${self.value_per_kg:.2f}/kg)"


@dataclass
class CargoAllocation:
    """Represents the loaded fraction of a cargo item."""
    item: CargoItem
    fraction_taken: float  # 0.0 to 1.0
    weight_taken: float
    value_taken: float

    def __repr__(self) -> str:
        return (f"Allocation({self.item.item_id}: {self.fraction_taken*100:.1f}% "
                f"({self.weight_taken:.1f}kg -> ${self.value_taken:.2f}))")


def fractional_knapsack(
    items: List[CargoItem],
    capacity: float
) -> Tuple[List[CargoAllocation], float, float, Dict[str, Any]]:
    """Greedy Fractional Knapsack Algorithm.

    Strategy:
    1. Compute ratio value / weight for all cargo items.
    2. Sort items descending by this ratio.
    3. Greedily load as much of the highest ratio item as possible until van is full.

    Time Complexity: O(n log n) sorting + O(n) greedy fill.
    Space Complexity: O(n) for allocations.
    """
    if capacity <= 0 or not items:
        return [], 0.0, 0.0, {"capacity": capacity, "used_capacity": 0.0, "total_value": 0.0}

    # Sort descending by value density (value per kg)
    sorted_items = sorted(items, key=lambda it: it.value_per_kg, reverse=True)

    allocations: List[CargoAllocation] = []
    remaining_capacity = float(capacity)
    total_value = 0.0
    total_weight = 0.0

    for item in sorted_items:
        if remaining_capacity <= 0:
            break

        if item.weight <= remaining_capacity:
            # Take entire item (fraction = 1.0)
            fraction = 1.0
            weight_taken = item.weight
            value_taken = item.value
        else:
            # Van capacity exhausted; take fractional slice
            fraction = remaining_capacity / item.weight
            weight_taken = remaining_capacity
            value_taken = item.value * fraction

        allocations.append(
            CargoAllocation(
                item=item,
                fraction_taken=fraction,
                weight_taken=weight_taken,
                value_taken=value_taken
            )
        )
        remaining_capacity -= weight_taken
        total_weight += weight_taken
        total_value += value_taken

    summary = {
        "van_capacity_kg": capacity,
        "total_weight_loaded_kg": round(total_weight, 2),
        "total_value_loaded_usd": round(total_value, 2),
        "capacity_utilization_pct": round((total_weight / capacity) * 100.0, 1),
        "items_fully_loaded": sum(1 for a in allocations if a.fraction_taken >= 1.0),
        "items_fractionally_loaded": sum(1 for a in allocations if 0.0 < a.fraction_taken < 1.0),
    }

    return allocations, total_value, total_weight, summary


def get_fractional_knapsack_limitation_note() -> str:
    """One-line note on why greedy ratio fails on 0/1 indivisible cargo.

    Required by the assessment deliverable checklist.
    """
    return (
        "Note on 0/1 Limitation: The greedy value-density heuristic fails for indivisible (0/1) cargo "
        "because an item with high density may consume an awkward capacity amount that prevents packing "
        "other items, leaving unused vehicle capacity that cannot be filled with fractions of remaining high-value items."
    )
