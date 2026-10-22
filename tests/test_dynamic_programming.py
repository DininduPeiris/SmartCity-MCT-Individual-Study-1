"""Unit tests for Dynamic Programming algorithms: 0/1 Knapsack & Bellman-Ford Routing."""

import unittest
from smartcity.dynamic_programming.knapsack_01 import (
    IndivisibleItem,
    knapsack_01_2d,
    knapsack_01_1d,
    knapsack_01_brute_force,
    compare_knapsack_implementations
)
from smartcity.dynamic_programming.shortest_path_dp import (
    CityGraph,
    bellman_ford_dp,
    reconstruct_path
)


class TestDynamicProgramming(unittest.TestCase):

    def test_knapsack_01_2d_and_1d_equivalence(self):
        """Verifies 2D table DP, 1D rolling array, and Brute Force yield identical optimal values."""
        items = [
            IndivisibleItem("ITM_A", "Server Rack", 10, 60),
            IndivisibleItem("ITM_B", "Lithium Battery Pack", 20, 100),
            IndivisibleItem("ITM_C", "Telecom Transmitter", 30, 120),
        ]
        capacity = 50

        # In 0/1 knapsack, optimal selection for W=50 is items B + C: weight = 20 + 30 = 50, value = 100 + 120 = 220
        # Notice greedy ratio would choose A (ratio 6) then B (ratio 5), giving only 60+100=160!
        val_2d, chosen, dp_table, stats_2d = knapsack_01_2d(items, capacity)
        val_1d, stats_1d = knapsack_01_1d(items, capacity)
        val_bf, bf_calls, bf_time = knapsack_01_brute_force(items, capacity)

        self.assertEqual(val_2d, 220)
        self.assertEqual(val_1d, 220)
        self.assertEqual(val_bf, 220)

        # Verify chosen items are ITM_B and ITM_C
        chosen_ids = {it.item_id for it in chosen}
        self.assertEqual(chosen_ids, {"ITM_B", "ITM_C"})

        # Verify genuine memory reduction
        self.assertLess(stats_1d["memory_bytes"], stats_2d["memory_bytes"])

    def test_knapsack_exponential_blowup_comparison(self):
        """Verifies benchmarking function executes and captures exponential call counts."""
        items = [
            IndivisibleItem(f"ITM_{i}", f"Cargo {i}", (i % 7) + 2, (i % 11) * 15 + 20)
            for i in range(12)
        ]
        comparison = compare_knapsack_implementations(items, capacity=40)
        self.assertEqual(comparison["max_value_2d"], comparison["max_value_1d"])
        self.assertEqual(comparison["max_value_2d"], comparison["max_value_bf"])
        self.assertGreater(comparison["bf_recursive_calls"], 1000)

    def test_bellman_ford_shortest_path(self):
        """Tests DP shortest path on a 5-node urban transit graph."""
        graph = CityGraph()
        # Add road edges: Central Depot (S) -> A, B, C, D
        graph.add_edge("DEPOT", "HUB_A", 4.0, "Expressway A")
        graph.add_edge("DEPOT", "HUB_B", 2.0, "Main Ring Road")
        graph.add_edge("HUB_A", "HUB_C", 3.0, "Commercial Boulevard")
        graph.add_edge("HUB_B", "HUB_A", 1.0, "Cross Connector")
        graph.add_edge("HUB_B", "HUB_C", 6.0, "Riverfront Bridge")
        graph.add_edge("HUB_B", "HUB_D", 7.0, "Industrial Ave")
        graph.add_edge("HUB_C", "HUB_D", 2.0, "Outer Link")

        distances, predecessors, has_neg, stats = bellman_ford_dp(graph, "DEPOT")

        self.assertFalse(has_neg)
        # Optimal paths:
        # DEPOT -> DEPOT: 0.0
        # DEPOT -> HUB_B: 2.0
        # DEPOT -> HUB_B -> HUB_A: 2.0 + 1.0 = 3.0 (shorter than direct edge of 4.0!)
        # DEPOT -> HUB_B -> HUB_A -> HUB_C: 3.0 + 3.0 = 6.0
        # DEPOT -> HUB_B -> HUB_A -> HUB_C -> HUB_D: 6.0 + 2.0 = 8.0
        self.assertEqual(distances["DEPOT"], 0.0)
        self.assertEqual(distances["HUB_B"], 2.0)
        self.assertEqual(distances["HUB_A"], 3.0)
        self.assertEqual(distances["HUB_C"], 6.0)
        self.assertEqual(distances["HUB_D"], 8.0)

        path_to_d = reconstruct_path(predecessors, "HUB_D")
        self.assertEqual(path_to_d, ["DEPOT", "HUB_B", "HUB_A", "HUB_C", "HUB_D"])

    def test_bellman_ford_negative_cycle(self):
        """Verifies detection of negative-cost cycles."""
        graph = CityGraph()
        graph.add_edge("A", "B", 1.0)
        graph.add_edge("B", "C", -3.0)
        graph.add_edge("C", "A", 1.0)  # Cycle A->B->C->A has weight 1 - 3 + 1 = -1

        distances, predecessors, has_neg, stats = bellman_ford_dp(graph, "A")
        self.assertTrue(has_neg)


if __name__ == "__main__":
    unittest.main()
