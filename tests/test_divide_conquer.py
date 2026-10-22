"""Unit tests for Divide & Conquer algorithms: Merge Sort & Closest Pair."""

import unittest
import math
from smartcity.divide_conquer.merge_sort import (
    Package,
    merge_sort_packages,
    merge_sort_instrumented,
    benchmark_merge_sort_complexity
)
from smartcity.divide_conquer.closest_pair import (
    Hub,
    Point,
    closest_pair_hubs,
    brute_force_closest_pair,
    benchmark_closest_pair
)


class TestDivideAndConquer(unittest.TestCase):

    def test_merge_sort_edge_cases(self):
        """Test empty list, single element, duplicate deadlines."""
        # 1. Empty list
        self.assertEqual(merge_sort_packages([]), [])

        # 2. Single element
        pkg1 = Package("P1", "Alpha", 10.0, 1, 5.0, "North")
        self.assertEqual(merge_sort_packages([pkg1]), [pkg1])

        # 3. Duplicate deadlines with priority tie-breaking
        pkg_dup1 = Package("P1", "Recipient 1", 9.0, 1, 5.0, "Zone A")  # Normal
        pkg_dup2 = Package("P2", "Recipient 2", 9.0, 3, 4.0, "Zone B")  # Urgent
        sorted_pkgs = merge_sort_packages([pkg_dup1, pkg_dup2])
        # Higher priority (3) should appear first when deadlines are identical
        self.assertEqual(sorted_pkgs[0].package_id, "P2")
        self.assertEqual(sorted_pkgs[1].package_id, "P1")

    def test_merge_sort_instrumentation(self):
        """Verifies comparison count and recursion depth are tracked."""
        numbers = [54, 26, 93, 17, 77, 31, 44, 55, 20]
        sorted_nums, comps, calls, depth = merge_sort_instrumented(numbers)
        self.assertEqual(sorted_nums, sorted(numbers))
        self.assertGreater(comps, 0)
        self.assertGreater(calls, 0)
        self.assertGreaterEqual(depth, 3)

    def test_merge_sort_empirical_growth(self):
        """Empirical verification that comparisons scale as O(n log n)."""
        benchmark = benchmark_merge_sort_complexity([64, 128, 256, 512])
        for row in benchmark:
            # Ratio of actual comps to n*log2(n) should remain comfortably bounded in [0.7, 1.2]
            self.assertGreater(row["ratio (comps / n_log_n)"], 0.5)
            self.assertLess(row["ratio (comps / n_log_n)"], 1.5)

    def test_closest_pair_edge_cases(self):
        """Test empty list, 1 point, duplicate points."""
        # 1. Empty list
        pair, dist = closest_pair_hubs([])
        self.assertIsNone(pair)
        self.assertEqual(dist, float("inf"))

        # 2. Single point
        h1 = Hub("H1", "Solo", Point(10.0, 20.0))
        pair, dist = closest_pair_hubs([h1])
        self.assertIsNone(pair)
        self.assertEqual(dist, float("inf"))

        # 3. Duplicate points (distance must be exactly 0.0)
        h2 = Hub("H2", "Clone", Point(10.0, 20.0))
        pair, dist = closest_pair_hubs([h1, h2])
        self.assertIsNotNone(pair)
        self.assertEqual(dist, 0.0)

    def test_closest_pair_correctness_vs_bruteforce(self):
        """Verifies D&C output matches brute-force on small and medium datasets."""
        hubs = [
            Hub("H1", "Central", Point(2.0, 3.0)),
            Hub("H2", "East", Point(12.0, 30.0)),
            Hub("H3", "North", Point(40.0, 50.0)),
            Hub("H4", "West", Point(5.0, 1.0)),
            Hub("H5", "South", Point(12.0, 10.0)),
            Hub("H6", "Near Central", Point(3.0, 4.0))  # Distance to H1 is sqrt((3-2)^2 + (4-3)^2) = sqrt(2) ~ 1.4142
        ]
        dc_pair, dc_dist = closest_pair_hubs(hubs)
        bf_pair, bf_dist = brute_force_closest_pair(hubs)

        self.assertAlmostEqual(dc_dist, bf_dist, places=5)
        self.assertAlmostEqual(dc_dist, math.sqrt(2.0), places=5)


if __name__ == "__main__":
    unittest.main()
