"""SmartCity Logistics - Integrated Optimization Dashboard.

Command-line dashboard wiring all modules together:
- Divide & Conquer: Merge Sort & Closest Pair
- Greedy: Activity Selection, Fractional Knapsack, Huffman Coding
- Dynamic Programming: 0/1 Knapsack & Bellman-Ford Shortest Path
"""

import os
import sys
import csv
import time
import argparse
from typing import List

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
from smartcity.dynamic_programming.knapsack_01 import (
    IndivisibleItem,
    knapsack_01_2d,
    knapsack_01_1d,
    compare_knapsack_implementations,
    trace_knapsack_table
)
from smartcity.dynamic_programming.shortest_path_dp import (
    CityGraph,
    bellman_ford_dp,
    reconstruct_path
)


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_packages_from_csv(csv_path: str) -> List[Package]:
    """Loads sample packages from CSV file."""
    packages = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            packages.append(
                Package(
                    package_id=row["package_id"],
                    recipient=row["recipient"],
                    deadline_hour=float(row["deadline_hour"]),
                    priority=int(row["priority"]),
                    weight_kg=float(row["weight_kg"]),
                    destination_zone=row["destination_zone"]
                )
            )
    return packages


def load_hubs_from_csv(csv_path: str) -> List[Hub]:
    """Loads sample hubs from CSV file."""
    hubs = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hubs.append(
                Hub(
                    hub_id=row["hub_id"],
                    name=row["name"],
                    location=Point(float(row["x_coord_km"]), float(row["y_coord_km"])),
                    capacity_daily_parcels=int(row["capacity_daily_parcels"])
                )
            )
    return hubs


def load_manifest_text(file_path: str) -> str:
    """Loads plain text delivery manifest."""
    with open(file_path, mode="r", encoding="utf-8") as f:
        return f.read()


# ==============================================================================
# CLI Interactive Menus & Module Runners
# ==============================================================================

def run_merge_sort_demo():
    print("\n" + "=" * 70)
    print(" [1] DIVIDE & CONQUER: WAREHOUSE QUEUE SORTING (MERGE SORT)")
    print("=" * 70)
    csv_file = os.path.join(DATA_DIR, "sample_packages.csv")
    packages = load_packages_from_csv(csv_file)
    print(f"Loaded {len(packages)} packages from {os.path.basename(csv_file)}.")

    print("\nUnsorted Warehouse Queue (first 5):")
    for p in packages[:5]:
        print(f"  {p}")

    sorted_pkgs = merge_sort_packages(packages)

    print("\nSorted Priority Dispatch Queue (first 10, earliest deadline & urgent prio):")
    for idx, p in enumerate(sorted_pkgs[:10], 1):
        prio_str = "URGENT" if p.priority == 3 else ("EXPRESS" if p.priority == 2 else "STANDARD")
        print(f"  {idx:02d}. [{p.deadline_hour:04.1f}h] {p.package_id} -> {p.recipient:<25} ({prio_str:<8}) {p.weight_kg:4.1f}kg")

    print("\n--- Empirical O(n log n) Verification ---")
    sizes = [16, 64, 256, 1024, 4096]
    benchmark = benchmark_merge_sort_complexity(sizes)
    print(f"{'n':>6} | {'Comparisons':>12} | {'n * log2(n)':>12} | {'Ratio':>8} | {'Depth':>6} | {'Calls':>8}")
    print("-" * 65)
    for b in benchmark:
        print(f"{b['n']:6d} | {b['comparisons']:12d} | {b['n_log2_n']:12.1f} | {b['ratio (comps / n_log_n)']:8.4f} | {b['max_depth']:6d} | {b['recursive_calls']:8d}")
    print("Empirical confirmation: Ratio of comparisons to theoretical n*log2(n) asymptotically converges to ~1.0.")


def run_closest_pair_demo():
    print("\n" + "=" * 70)
    print(" [2] DIVIDE & CONQUER: CLOSEST PAIR OF LOGISTICS HUBS (2D GEOMETRY)")
    print("=" * 70)
    csv_file = os.path.join(DATA_DIR, "sample_hubs.csv")
    hubs = load_hubs_from_csv(csv_file)
    print(f"Loaded {len(hubs)} urban distribution hubs from {os.path.basename(csv_file)}.")

    pair, dist = closest_pair_hubs(hubs)
    if pair:
        h1, h2 = pair
        print(f"\nClosest Hub Pair Identified (Divide & Conquer):")
        print(f"  Hub 1: {h1.hub_id} ({h1.name}) at ({h1.x:.2f}, {h1.y:.2f})")
        print(f"  Hub 2: {h2.hub_id} ({h2.name}) at ({h2.x:.2f}, {h2.y:.2f})")
        print(f"  Direct Distance: {dist:.4f} km")
        print(f"  Logistics Action: Candidates for micro-shuttle route consolidation.")

    print("\n--- Benchmark Table: Divide & Conquer O(n log n) vs Brute Force O(n^2) ---")
    bench = benchmark_closest_pair([100, 500, 1000, 2000])
    print(f"{'N Points':>10} | {'D&C Time (ms)':>15} | {'Brute Force (ms)':>18} | {'Speedup':>10} | {'Dist Match':>12}")
    print("-" * 75)
    for row in bench:
        print(f"{row['n']:10d} | {row['dc_time_ms']:15.3f} | {row['bf_time_ms']:18.3f} | {row['speedup_factor']:9.1f}x | {str(row['distances_match']):>12}")
    print("Confirmation: D&C maintains sub-millisecond scaling while Brute-Force exhibits quadratic growth.")


def run_activity_selection_demo():
    print("\n" + "=" * 70)
    print(" [3] GREEDY: DRIVER FLEET SCHEDULING (ACTIVITY SELECTION)")
    print("=" * 70)
    shift_jobs = [
        DeliveryJob("JOB_01", "Morning Hospital Drop", 8.0, 9.5, "City Hospital"),
        DeliveryJob("JOB_02", "Express Pharma Run", 8.5, 9.0, "St. Jude Pharmacy"),
        DeliveryJob("JOB_03", "Tech Park Component Transfer", 9.0, 11.0, "Apex Tech Labs"),
        DeliveryJob("JOB_04", "Retail Center Restock", 9.5, 10.5, "Metro Center"),
        DeliveryJob("JOB_05", "Harbor Perishables Intake", 10.0, 12.0, "North Harbor"),
        DeliveryJob("JOB_06", "Financial Core Courier Run", 11.0, 12.5, "Financial Station"),
        DeliveryJob("JOB_07", "University Research Reagents", 12.0, 13.5, "University Cluster"),
        DeliveryJob("JOB_08", "Downtown Legal Documents", 13.0, 14.0, "City Hall Archives"),
        DeliveryJob("JOB_09", "Outer Industrial Bulk Drop", 13.5, 16.0, "Industrial Park"),
        DeliveryJob("JOB_10", "Suburban Last-Mile Dispatch", 14.0, 15.5, "Suburban Hub"),
        DeliveryJob("JOB_11", "Evening Data Center Server Rack", 15.5, 17.5, "Summit Data Center"),
        DeliveryJob("JOB_12", "Night Airport Freight Handover", 17.0, 19.0, "Aerospace Terminal"),
    ]

    selected, stats = activity_selection_earliest_finish(shift_jobs)

    print(f"Considered {stats['total_considered']} candidate delivery requests.")
    print(f"Greedy Earliest-Finish-Time Selected {stats['total_selected']} non-overlapping jobs:")
    for idx, job in enumerate(selected, 1):
        print(f"  {idx:02d}. [{job.start_time:04.1f}h - {job.end_time:04.1f}h] {job.job_id} ({job.description}) -> {job.destination}")

    print(f"\nDriver Active Shift Time: {stats['driver_utilization_hours']:.1f} hours.")
    print(f"Shift Scheduling Efficiency: {stats['selection_efficiency_pct']}% of jobs served.")
    print("\n" + get_activity_selection_justification())


def run_fractional_knapsack_demo():
    print("\n" + "=" * 70)
    print(" [4] GREEDY: LOADING DELIVERY VAN WITH DIVISIBLE CARGO")
    print("=" * 70)
    items = [
        CargoItem("BULK_01", "Medical Diagnostic Solutions", 30.0, 450.0), # $15.0/kg
        CargoItem("BULK_02", "Specialty Lubricants & Fluids", 40.0, 480.0), # $12.0/kg
        CargoItem("BULK_03", "Precision Tooling Calibrators", 20.0, 360.0), # $18.0/kg
        CargoItem("BULK_04", "Organic Raw Pharmaceuticals", 15.0, 375.0),    # $25.0/kg
        CargoItem("BULK_05", "Sanitary PPE Aggregates", 50.0, 300.0),       # $6.0/kg
        CargoItem("BULK_06", "Recycled Packaging Pellets", 60.0, 240.0),    # $4.0/kg
    ]
    van_capacity = 100.0  # kg

    print(f"Van Maximum Payload: {van_capacity} kg.")
    print("\nAvailable Divisible Cargo Inventory:")
    for it in sorted(items, key=lambda x: x.value_per_kg, reverse=True):
        print(f"  {it.item_id:<8} | {it.name:<32} | {it.weight:5.1f} kg | ${it.value:7.2f} | (${it.value_per_kg:5.2f}/kg)")

    allocations, total_val, total_wt, stats = fractional_knapsack(items, van_capacity)

    print(f"\nGreedy Loading Plan (Maximized Value):")
    for a in allocations:
        status = "FULL" if a.fraction_taken >= 1.0 else f"PARTIAL ({a.fraction_taken*100:.1f}%)"
        print(f"  {a.item.item_id:<8} | {a.item.name:<32} | {a.weight_taken:5.1f} kg loaded | ${a.value_taken:7.2f} | [{status}]")

    print(f"\nTotal Weight Loaded: {total_wt:.1f} / {van_capacity:.1f} kg ({stats['capacity_utilization_pct']}%)")
    print(f"Total Economic Value Realized: ${total_val:.2f}")
    print("\n" + get_fractional_knapsack_limitation_note())


def run_huffman_demo():
    print("\n" + "=" * 70)
    print(" [5] GREEDY: COMPRESSING TELEMATICS MANIFESTS (HUFFMAN CODING)")
    print("=" * 70)
    manifest_path = os.path.join(DATA_DIR, "sample_manifest.txt")
    manifest_text = load_manifest_text(manifest_path)

    huffman = HuffmanCoding()
    encoded_bits, stats = huffman.compress_manifest(manifest_text)
    decoded_text = huffman.decode(encoded_bits)

    print(f"Original Manifest Size: {stats['original_size_bytes']} bytes ({stats['original_size_bits']} bits)")
    print(f"Compressed Bitstream:   {stats['compressed_size_bytes']} bytes ({stats['compressed_size_bits']} bits)")
    print(f"Compression Ratio:      {stats['compression_ratio']:.4f} ({stats['compression_ratio']*100:.2f}% of original)")
    print(f"Bandwidth Space Saving: {stats['space_saving_percentage']:.2f}%")
    print(f"Lossless Verification:  {'PASSED [Lossless Decoded Matches Character-for-Character]' if stats['is_lossless'] else 'FAILED'}")

    print("\nSample Huffman Prefix Codes (Top 8 most frequent symbols):")
    for ch, code in list(stats["codebook_sample"].items())[:8]:
        repr_ch = repr(ch) if ch in ('\n', ' ', '\t') else f"'{ch}'"
        freq = huffman.frequencies.get(ch, 0)
        print(f"  Symbol: {repr_ch:<6} | Frequency: {freq:4d} | Huffman Bitcode: {code}")


def run_knapsack_01_demo():
    print("\n" + "=" * 70)
    print(" [6] DYNAMIC PROGRAMMING: 0/1 INDIVISIBLE CARGO OPTIMIZATION")
    print("=" * 70)
    items = [
        IndivisibleItem("CARGO_A", "Automated Defibrillator", 10, 60),
        IndivisibleItem("CARGO_B", "Cryogenic Nitrogen Flask", 20, 100),
        IndivisibleItem("CARGO_C", "Satellite Receiver Array", 30, 120),
        IndivisibleItem("CARGO_D", "High-Power Drone Hub", 15, 75),
        IndivisibleItem("CARGO_E", "Backup Battery Storage", 25, 110),
    ]
    capacity = 50

    print(f"Delivery Vehicle Indivisible Capacity: {capacity} kg")
    print("Items Available:")
    for it in items:
        print(f"  {it}")

    # Benchmark 2D vs 1D vs Recursive Brute Force
    comp = compare_knapsack_implementations(items, capacity)
    print("\nComparison Results:")
    print(f"  2D DP Optimal Value:           ${comp['max_value_2d']} (Runtime: {comp['runtime_2d_ms']:.4f} ms, Memory: {comp['memory_2d_bytes']} bytes)")
    print(f"  1D Rolling DP Optimal Value:   ${comp['max_value_1d']} (Runtime: {comp['runtime_1d_ms']:.4f} ms, Memory: {comp['memory_1d_bytes']} bytes)")
    print(f"  Recursive Brute-Force Value:   ${comp['max_value_bf']} (Runtime: {comp['runtime_bf_ms']} ms, Recursive Calls: {comp['bf_recursive_calls']})")
    print(f"  Genuine Memory Reduction:      {comp['memory_reduction_pct']}% savings with 1D rolling array!")

    print("\nOptimal Cargo Items Selected for Loading:")
    for it in comp["chosen_items"]:
        print(f"  [X] {it.item_id}: {it.name:<28} | Wt: {it.weight:2d}kg | Val: ${it.value}")

    print("\n--- Hand-Traceable 2D Dynamic Programming Table Trace ---")
    headers, dp_matrix = trace_knapsack_table(items[:3], capacity=50)
    print(f"{'Item':<20} | " + " | ".join(f"{w:3d}" for w in range(0, 51, 10)))
    print("-" * 55)
    row_names = ["0: Initial State"] + [f"{i}: {items[i-1].item_id}" for i in range(1, 4)]
    for i in range(4):
        sampled_vals = [f"{dp_matrix[i][w]:3d}" for w in range(0, 51, 10)]
        print(f"{row_names[i]:<20} | " + " | ".join(sampled_vals))


def run_bellman_ford_demo():
    print("\n" + "=" * 70)
    print(" [7] DYNAMIC PROGRAMMING: URBAN NETWORK ROUTING (BELLMAN-FORD)")
    print("=" * 70)
    graph = CityGraph()
    edges = [
        ("HUB_01 (Central)", "HUB_02 (North Harbor)", 18.5, "North Corridor Tollway"),
        ("HUB_01 (Central)", "HUB_03 (Uptown)", 12.0, "Uptown Arterial"),
        ("HUB_01 (Central)", "HUB_07 (West Hills)", 15.0, "West Highway"),
        ("HUB_02 (North Harbor)", "HUB_05 (Airport)", 14.0, "Coastal Beltway"),
        ("HUB_03 (Uptown)", "HUB_02 (North Harbor)", 9.5, "Harbor Link"),
        ("HUB_03 (Uptown)", "HUB_11 (Tech Corridor)", 8.0, "Metro Expressway"),
        ("HUB_07 (West Hills)", "HUB_08 (South-West)", 11.0, "Valley Bypass"),
        ("HUB_11 (Tech Corridor)", "HUB_05 (Airport)", 7.5, "Tech Aero Shuttleway"),
        ("HUB_11 (Tech Corridor)", "HUB_04 (East Depot)", 13.0, "East Ring Road"),
        ("HUB_08 (South-West)", "HUB_06 (South River)", 10.0, "River Crossing"),
        ("HUB_06 (South River)", "HUB_04 (East Depot)", 16.0, "Southern Ring"),
    ]
    for src, dst, wt, name in edges:
        graph.add_edge(src, dst, wt, name)

    source = "HUB_01 (Central)"
    distances, predecessors, has_neg, stats = bellman_ford_dp(graph, source)

    print(f"Source Hub: {source}")
    print(f"Network Summary: {stats['vertex_count']} Vertices, {stats['edge_count']} Directed Edges")
    print(f"Negative Cycle Detected: {has_neg}")
    print(f"DP Relaxations Completed in {stats['iterations_run']} Passes (Upper bound: {stats['max_possible_iterations']})")

    print("\nOptimal Shortest Delivery Routes:")
    print(f"{'Destination Hub':<28} | {'Min Transit Time':>18} | {'Optimal Route Path'}")
    print("-" * 80)
    for dst in sorted(graph.vertices):
        if dst == source:
            continue
        cost = distances[dst]
        path = reconstruct_path(predecessors, dst)
        path_str = " -> ".join(p.split()[0] for p in path)
        cost_str = f"{cost:.1f} mins" if cost < float("inf") else "UNREACHABLE"
        print(f"{dst:<28} | {cost_str:>18} | {path_str}")


def run_full_pipeline():
    """Executes all modules end-to-end sequentially."""
    print("\n" + "#" * 70)
    print(" RUNNING COMPLETE SMARTCITY LOGISTICS PIPELINE")
    print("#" * 70)
    run_merge_sort_demo()
    run_closest_pair_demo()
    run_activity_selection_demo()
    run_fractional_knapsack_demo()
    run_huffman_demo()
    run_knapsack_01_demo()
    run_bellman_ford_demo()
    print("\n" + "#" * 70)
    print(" ALL MODULES COMPLETED SUCCESSFULLY!")
    print("#" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(description="SmartCity Logistics Algorithmic Optimization Suite")
    parser.add_argument("--all", action="store_true", help="Run entire pipeline non-interactively")
    parser.add_argument("--module", type=int, choices=range(1, 8), help="Run a specific module (1-7)")
    args = parser.parse_args()

    if args.all:
        run_full_pipeline()
        return

    if args.module:
        dispatch = {
            1: run_merge_sort_demo,
            2: run_closest_pair_demo,
            3: run_activity_selection_demo,
            4: run_fractional_knapsack_demo,
            5: run_huffman_demo,
            6: run_knapsack_01_demo,
            7: run_bellman_ford_demo,
        }
        dispatch[args.module]()
        return

    # Interactive CLI Menu
    while True:
        print("\n" + "=" * 60)
        print("    SMARTCITY LOGISTICS - ALGORITHMIC OPTIMIZATION SUITE")
        print("=" * 60)
        print(" 1. Warehouse Dispatch Queue Sorting (Merge Sort D&C)")
        print(" 2. Distribution Hub Proximity Matching (Closest Pair D&C)")
        print(" 3. Driver Shift Scheduling (Activity Selection Greedy)")
        print(" 4. Vehicle Divisible Cargo Loading (Fractional Knapsack Greedy)")
        print(" 5. Manifest Telematics Compression (Huffman Coding Greedy)")
        print(" 6. Indivisible High-Value Cargo Loading (0/1 Knapsack DP)")
        print(" 7. Metropolitan Urban Routing (Bellman-Ford DP)")
        print(" 8. Execute Full End-to-End Logistics Pipeline")
        print(" 9. Run Automated Test Suite (Unittest)")
        print(" 0. Exit")
        print("-" * 60)
        choice = input("Enter choice (0-9): ").strip()

        if choice == "1":
            run_merge_sort_demo()
        elif choice == "2":
            run_closest_pair_demo()
        elif choice == "3":
            run_activity_selection_demo()
        elif choice == "4":
            run_fractional_knapsack_demo()
        elif choice == "5":
            run_huffman_demo()
        elif choice == "6":
            run_knapsack_01_demo()
        elif choice == "7":
            run_bellman_ford_demo()
        elif choice == "8":
            run_full_pipeline()
        elif choice == "9":
            import unittest
            suite = unittest.defaultTestLoader.discover(os.path.join(os.path.dirname(__file__), "tests"))
            unittest.TextTestRunner(verbosity=2).run(suite)
        elif choice == "0":
            print("\nExiting SmartCity Logistics Dashboard. Goodbye!\n")
            break
        else:
            print("Invalid choice, please select between 0 and 9.")


if __name__ == "__main__":
    main()
