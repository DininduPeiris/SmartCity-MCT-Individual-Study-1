# SmartCity Logistics - Algorithmic Optimization Suite

This repository implements the complete algorithmic backbone for **SmartCity Logistics**, an urban delivery, warehouse routing, and fleet scheduling system. The project covers three core design paradigms—**Divide & Conquer**, **Greedy Algorithms**, and **Dynamic Programming**—integrated into a unified command-line dashboard.

---

## 1. System Architecture & Features

| Module | Algorithmic Paradigm | Purpose & Logistics Feature |
| :--- | :--- | :--- |
| **Warehouse Queue Dispatch** | **Divide & Conquer** | Sorts packages arriving in random order by delivery deadline and priority tier using recursive Merge Sort. |
| **Logistics Hub Clustering** | **Divide & Conquer** | Computes the closest pair of distribution hubs in 2D space ($O(n \log n)$) to enable shuttle route consolidation. |
| **Driver Fleet Scheduling** | **Greedy** | Schedules maximum mutually compatible delivery jobs per driver using the Earliest Finish Time (EFT) policy. |
| **Divisible Van Loading** | **Greedy** | Maximizes loaded cargo value for divisible goods under vehicle payload constraints using value/weight density. |
| **Manifest Compression** | **Greedy** | Compresses shipment manifests and telematics data using Huffman prefix coding for efficient cellular transmission. |
| **Indivisible Cargo Loading** | **Dynamic Programming** | Optimizes loading of high-value indivisible equipment (0/1 Knapsack) using 2D and memory-optimized 1D rolling array DP. |
| **Metropolitan Road Routing**| **Dynamic Programming** | Computes least-cost/fastest transit routes from the central depot across a directed urban graph via Bellman-Ford DP. |

---

## 2. Algorithmic Complexity Summary

| Component | Time Complexity (Best) | Time Complexity (Average) | Time Complexity (Worst) | Space Complexity |
| :--- | :---: | :---: | :---: | :---: |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| **Closest Pair of 2D Hubs** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| **Closest Pair (Brute Force)** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ |
| **Activity Selection (Greedy EFT)** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| **Fractional Knapsack (Greedy)** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| **Huffman Coding (Tree & Encoding)**| $O(n + k \log k)$ | $O(n + k \log k)$ | $O(n + k \log k)$ | $O(k)$ |
| **0/1 Knapsack (2D Table DP)** | $O(n \cdot W)$ | $O(n \cdot W)$ | $O(n \cdot W)$ | $O(n \cdot W)$ |
| **0/1 Knapsack (1D Rolling DP)** | $O(n \cdot W)$ | $O(n \cdot W)$ | $O(n \cdot W)$ | $O(W)$ |
| **0/1 Knapsack (Recursive Brute-Force)**| $O(2^n)$ | $O(2^n)$ | $O(2^n)$ | $O(n)$ stack |
| **Bellman-Ford Shortest Path DP** | $O(\|V\| \cdot \|E\|)$ | $O(\|V\| \cdot \|E\|)$ | $O(\|V\| \cdot \|E\|)$ | $O(\|V\|)$ |

*Note: $n$ = item/hub count, $k$ = distinct alphabet characters, $W$ = knapsack integer capacity, $\|V\|$ = graph vertices, $\|E\|$ = graph directed edges.*

---

## 3. Directory Layout

```
smartcity/
├── divide_conquer/
│   ├── __init__.py
│   ├── merge_sort.py           # Recursive merge sort + comparison counter instrumentation
│   └── closest_pair.py         # O(n log n) 2D closest pair + O(n^2) brute force benchmark
├── greedy/
│   ├── __init__.py
│   ├── activity_selection.py   # Earliest finish time scheduling + exchange argument
│   ├── fractional_knapsack.py  # Greedy value-density cargo loading + 0/1 limitation note
│   └── huffman.py              # Priority queue Huffman prefix encoding + lossless decoder
├── dynamic_programming/
│   ├── __init__.py
│   ├── knapsack_01.py          # 2D DP, 1D rolling array, recursive brute force & table trace
│   └── shortest_path_dp.py     # Bellman-Ford DP formulation & route reconstruction
├── data/
│   ├── sample_packages.csv     # 25 real-world logistics packages
│   ├── sample_hubs.csv         # 20 urban distribution centers with 2D coordinates
│   └── sample_manifest.txt     # Complete dispatch manifest text
├── tests/
│   ├── __init__.py
│   ├── test_divide_conquer.py  # Unit tests for D&C algorithms & edge cases
│   ├── test_greedy.py          # Unit tests for greedy algorithms & losslessness
│   └── test_dynamic_programming.py # Unit tests for DP algorithms & equivalence
├── main.py                     # Integrated interactive CLI dashboard
└── README.md                   # System documentation & complexity summary
```

---

## 4. Execution Instructions

### Running the Interactive Dashboard
Launch the unified SmartCity command-line interface:
```bash
python smartcity/main.py
```

### Running All Modules Non-Interactively
Execute the complete end-to-end demonstration across all 7 algorithmic tasks:
```bash
python smartcity/main.py --all
```

### Running a Specific Module
Run any single module (1 to 7):
```bash
python smartcity/main.py --module 1   # Run Merge Sort & Empirical Complexity
python smartcity/main.py --module 2   # Run Closest Pair D&C vs Brute-force
python smartcity/main.py --module 6   # Run 0/1 Knapsack 2D vs 1D vs Brute Force
```

### Running Automated Test Suite
Run all unit tests with verbose test execution reporting:
```bash
python -m unittest discover -s smartcity/tests -v
```
