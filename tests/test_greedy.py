"""Unit tests for Greedy algorithms: Activity Selection, Fractional Knapsack, Huffman Coding."""

import unittest
from smartcity.greedy.activity_selection import (
    DeliveryJob,
    activity_selection_earliest_finish,
    get_activity_selection_justification
)
from smartcity.greedy.fractional_knapsack import (
    CargoItem,
    fractional_knapsack,
    get_fractional_knapsack_limitation_note
)
from smartcity.greedy.huffman import HuffmanCoding


class TestGreedyAlgorithms(unittest.TestCase):

    def test_activity_selection(self):
        """Test scheduling non-overlapping delivery jobs."""
        jobs = [
            DeliveryJob("J1", "Morning Express", 1.0, 4.0, "Zone A"),
            DeliveryJob("J2", "Quick Drop", 3.0, 5.0, "Zone B"),
            DeliveryJob("J3", "Midday Dispatch", 0.0, 6.0, "Zone C"),
            DeliveryJob("J4", "Early Afternoon", 5.0, 7.0, "Zone D"),
            DeliveryJob("J5", "Rush Hour", 3.0, 9.0, "Zone E"),
            DeliveryJob("J6", "Evening Route", 5.0, 9.0, "Zone F"),
            DeliveryJob("J7", "Night Cargo", 6.0, 10.0, "Zone G"),
            DeliveryJob("J8", "Late Night", 8.0, 11.0, "Zone H"),
            DeliveryJob("J9", "Midnight Priority", 8.0, 12.0, "Zone I"),
            DeliveryJob("J10", "Last Mile", 2.0, 14.0, "Zone J"),
            DeliveryJob("J11", "Overnight Depot", 12.0, 16.0, "Zone K")
        ]
        selected, stats = activity_selection_earliest_finish(jobs)
        # Optimal schedule can pick 4 jobs: e.g., J1 (1-4), J4 (5-7), J8 (8-11), J11 (12-16)
        self.assertEqual(len(selected), 4)

        # Verify no two selected jobs overlap
        for i in range(len(selected) - 1):
            self.assertLessEqual(selected[i].end_time, selected[i + 1].start_time)

        # Verify justification text is present
        justification = get_activity_selection_justification()
        self.assertIn("Exchange Argument", justification)

    def test_fractional_knapsack(self):
        """Test greedy fractional loading of divisible goods."""
        items = [
            CargoItem("ITEM_1", "Medical Solutions", 10.0, 60.0),   # $6.0/kg
            CargoItem("ITEM_2", "Precision Tools", 20.0, 100.0),    # $5.0/kg
            CargoItem("ITEM_3", "Bulk Grain", 30.0, 120.0)          # $4.0/kg
        ]
        capacity = 50.0
        allocations, total_val, total_wt, stats = fractional_knapsack(items, capacity)

        # Optimal: ITEM_1 full (10kg, $60), ITEM_2 full (20kg, $100), ITEM_3 2/3 (20kg, $80)
        # Total value = 60 + 100 + 80 = $240.0, total weight = 50.0kg
        self.assertAlmostEqual(total_val, 240.0, places=2)
        self.assertAlmostEqual(total_wt, 50.0, places=2)
        self.assertEqual(stats["items_fully_loaded"], 2)
        self.assertEqual(stats["items_fractionally_loaded"], 1)

        # Limitation note check
        note = get_fractional_knapsack_limitation_note()
        self.assertIn("0/1", note)

    def test_huffman_coding_lossless(self):
        """Test Huffman encode, decode, losslessness, and compression."""
        huffman = HuffmanCoding()
        sample_text = "SMARTCITY LOGISTICS DISPATCH SYSTEM - RAPID ROUTING & PARCEL DELIVERY"

        encoded, stats = huffman.compress_manifest(sample_text)
        decoded = huffman.decode(encoded)

        self.assertEqual(decoded, sample_text)
        self.assertTrue(stats["is_lossless"])
        self.assertGreater(stats["space_saving_percentage"], 20.0)
        self.assertLess(stats["compression_ratio"], 0.8)

    def test_huffman_single_character(self):
        """Test edge case with repeated single character."""
        huffman = HuffmanCoding()
        text = "AAAAAAA"
        encoded, stats = huffman.compress_manifest(text)
        decoded = huffman.decode(encoded)
        self.assertEqual(decoded, text)


if __name__ == "__main__":
    unittest.main()
