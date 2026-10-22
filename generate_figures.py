"""Generates high-resolution publication-quality figures for the MCT 2101 Independent Study Report."""

import os
import matplotlib.pyplot as plt
import numpy as np

# Use clean classic styling
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300
})

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "report_assets"))
os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_mergesort_chart():
    """Generates comparison count vs theoretical n log2(n) plot."""
    n_vals = np.array([16, 32, 64, 128, 256, 512, 1024, 2048, 4096])
    # Actual comparisons from instrumented merge sort
    # Theoretical n*log2(n) - n + 1 (average merge sort comparisons)
    actual_comps = np.array([49, 120, 283, 658, 1506, 3397, 7559, 16684, 36582])
    theoretical = n_vals * np.log2(n_vals)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(n_vals, actual_comps, 'o-', color='#1f77b4', linewidth=2, markersize=6, label='Empirical Comparisons $C(n)$')
    ax.plot(n_vals, theoretical, '--', color='#d62728', linewidth=1.8, label='Theoretical Bound $n \log_2(n)$')

    ax.set_xscale('log', base=2)
    ax.set_yscale('log', base=10)
    ax.set_xlabel('Input Size $n$ (Packages in Queue, $\log_2$ scale)')
    ax.set_ylabel('Number of Key Comparisons ($\log_{10}$ scale)')
    ax.set_title('Figure 2.1: Merge Sort Empirical Comparisons vs. Theoretical $O(n \log n)$')
    ax.grid(True, which="both", ls=":", alpha=0.6)
    ax.legend(loc='upper left', frameon=True)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_mergesort_complexity.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"Saved: {path}")


def generate_closest_pair_chart():
    """Generates D&C O(n log n) vs Brute Force O(n^2) runtime benchmark plot."""
    n_points = np.array([100, 250, 500, 750, 1000, 1500, 2000])
    # Benchmark times in milliseconds
    dc_times = np.array([0.49, 1.45, 3.56, 5.42, 7.68, 13.10, 18.98])
    bf_times = np.array([0.64, 4.12, 17.08, 40.50, 73.73, 172.40, 320.09])

    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(n_points, dc_times, 's-', color='#2ca02c', linewidth=2, markersize=6, label='Divide & Conquer $O(n \log n)$')
    ax.plot(n_points, bf_times, '^-', color='#d62728', linewidth=2, markersize=6, label='Brute-Force All-Pairs $O(n^2)$')

    ax.set_xlabel('Number of Logistics Hubs ($n$)')
    ax.set_ylabel('Execution Time (milliseconds)')
    ax.set_title('Figure 2.2: Hub Proximity Matching Runtime: D&C vs. Brute-Force')
    ax.grid(True, ls=":", alpha=0.6)
    ax.legend(loc='upper left', frameon=True)

    # Annotate speedup at n=2000
    ax.annotate('16.9x Speedup\n(320 ms vs 19 ms)', xy=(2000, 19), xytext=(1450, 120),
                arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_closest_pair_benchmark.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"Saved: {path}")


def generate_knapsack_comparison_chart():
    """Generates bar chart comparing 2D DP vs 1D Rolling DP memory and runtime."""
    labels = ['2D Table DP\n$O(n \cdot W)$', '1D Rolling DP\n$O(W)$', 'Brute Force\n$O(2^n)$ (n=20)']
    memory_kb = [2.904, 0.464, 0.120]  # KB
    runtime_ms = [0.041, 0.012, 18.42]  # ms

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 3.8))

    # Memory comparison
    colors_mem = ['#1f77b4', '#2ca02c', '#7f7f7f']
    bars1 = ax1.bar(labels[:2], memory_kb[:2], color=colors_mem[:2], width=0.55, edgecolor='black', linewidth=0.8)
    ax1.set_ylabel('Memory Consumption (Kilobytes)')
    ax1.set_title('Auxiliary Memory (Capacity W=50)')
    ax1.grid(axis='y', ls=':', alpha=0.6)
    for bar in bars1:
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2.0, yval + 0.08, f"{yval:.2f} KB", ha='center', va='bottom', fontsize=9)
    ax1.text(0.5, 1.8, '84.0% Space\nSavings', ha='center', color='#2ca02c', fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#e8f5e9', edgecolor='#2ca02c'))

    # Runtime comparison (log scale due to brute-force blowup)
    colors_time = ['#1f77b4', '#2ca02c', '#d62728']
    bars2 = ax2.bar(labels, runtime_ms, color=colors_time, width=0.55, edgecolor='black', linewidth=0.8)
    ax2.set_yscale('log')
    ax2.set_ylabel('Execution Time in ms ($\log_{10}$ scale)')
    ax2.set_title('Runtime Comparison ($n=20$ Items)')
    ax2.grid(axis='y', ls=':', alpha=0.6)
    for bar in bars2:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval * 1.3, f"{yval:.3f} ms", ha='center', va='bottom', fontsize=9)

    fig.suptitle('Figure 2.3: 0/1 Knapsack Complexity & Optimization Profiles', fontsize=12)
    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_knapsack_comparison.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"Saved: {path}")


def generate_activity_schedule_chart():
    """Generates Gantt timeline chart for Greedy Activity Selection."""
    all_jobs = [
        ("JOB_01", 8.0, 9.5, False, "Hospital Drop"),
        ("JOB_02", 8.5, 9.0, True, "Express Pharma"),
        ("JOB_03", 9.0, 11.0, False, "Tech Park Transfer"),
        ("JOB_04", 9.5, 10.5, True, "Retail Restock"),
        ("JOB_05", 10.0, 12.0, False, "Harbor Intake"),
        ("JOB_06", 11.0, 12.5, True, "Financial Core"),
        ("JOB_07", 12.0, 13.5, False, "Univ. Research"),
        ("JOB_08", 13.0, 14.0, True, "Legal Documents"),
        ("JOB_09", 13.5, 16.0, False, "Industrial Drop"),
        ("JOB_10", 14.0, 15.5, True, "Suburban Dispatch"),
        ("JOB_11", 15.5, 17.5, True, "Server Rack"),
        ("JOB_12", 17.0, 19.0, False, "Airport Freight")
    ]

    fig, ax = plt.subplots(figsize=(8.5, 4.5))

    y_positions = range(len(all_jobs))
    for idx, (jid, start, end, selected, desc) in enumerate(reversed(all_jobs)):
        color = '#2ca02c' if selected else '#aec7e8'
        edgecolor = '#1b5e20' if selected else '#4682b4'
        linewidth = 1.5 if selected else 0.8
        alpha = 0.95 if selected else 0.6
        bar = ax.barh(idx, end - start, left=start, height=0.6, color=color,
                      edgecolor=edgecolor, linewidth=linewidth, alpha=alpha)
        label_text = f"{jid}: {desc}" + (" [SELECTED]" if selected else " [SKIPPED]")
        fontweight = 'bold' if selected else 'normal'
        ax.text(start + 0.1, idx, label_text, va='center', ha='left', fontsize=8.5,
                color='black' if not selected else 'white', fontweight=fontweight)

    ax.set_yticks(range(len(all_jobs)))
    ax.set_yticklabels([j[0] for j in reversed(all_jobs)])
    ax.set_xlabel('Driver Shift Hours (24-Hour Decimal Time, 08:00 - 19:00)')
    ax.set_title('Figure 2.4: Driver Shift Activity Selection Timeline (Earliest Finish Time)')
    ax.set_xlim(7.5, 19.5)
    ax.grid(axis='x', ls=':', alpha=0.6)

    # Custom legend
    import matplotlib.patches as mpatches
    green_patch = mpatches.Patch(color='#2ca02c', label='Selected Job (Maximal Non-Overlapping Set)')
    blue_patch = mpatches.Patch(color='#aec7e8', label='Incompatible / Conflicting Candidate Job')
    ax.legend(handles=[green_patch, blue_patch], loc='lower right', frameon=True)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_activity_schedule.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"Saved: {path}")


def generate_city_routing_graph():
    """Generates topological diagram of urban city logistics routing graph."""
    nodes = {
        "HUB_01\n(Central Depot)": (0, 0),
        "HUB_03\n(Uptown)": (2, 2),
        "HUB_02\n(Harbor)": (2, 4),
        "HUB_07\n(West Hills)": (-2, -1.5),
        "HUB_08\n(South-West)": (-1, -3.5),
        "HUB_06\n(South River)": (1.5, -3.5),
        "HUB_11\n(Tech Corridor)": (4, 1),
        "HUB_05\n(Airport)": (5, 3.5),
        "HUB_04\n(East Depot)": (4.5, -2)
    }

    fig, ax = plt.subplots(figsize=(8.5, 5.5))

    # Directed edges: (u, v, weight, is_shortest_tree)
    edges = [
        ("HUB_01\n(Central Depot)", "HUB_02\n(Harbor)", 18.5, True),
        ("HUB_01\n(Central Depot)", "HUB_03\n(Uptown)", 12.0, True),
        ("HUB_01\n(Central Depot)", "HUB_07\n(West Hills)", 15.0, True),
        ("HUB_02\n(Harbor)", "HUB_05\n(Airport)", 14.0, False),
        ("HUB_03\n(Uptown)", "HUB_02\n(Harbor)", 9.5, False),
        ("HUB_03\n(Uptown)", "HUB_11\n(Tech Corridor)", 8.0, True),
        ("HUB_07\n(West Hills)", "HUB_08\n(South-West)", 11.0, True),
        ("HUB_11\n(Tech Corridor)", "HUB_05\n(Airport)", 7.5, True),
        ("HUB_11\n(Tech Corridor)", "HUB_04\n(East Depot)", 13.0, True),
        ("HUB_08\n(South-West)", "HUB_06\n(South River)", 10.0, True),
        ("HUB_06\n(South River)", "HUB_04\n(East Depot)", 16.0, False),
    ]

    for u, v, w, in_tree in edges:
        x1, y1 = nodes[u]
        x2, y2 = nodes[v]
        dx = x2 - x1
        dy = y2 - y1
        color = '#d62728' if in_tree else '#9e9e9e'
        width = 2.2 if in_tree else 1.0
        style = '-' if in_tree else '--'

        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, lw=width, ls=style, shrinkA=18, shrinkB=18,
                                    mutation_scale=15))
        # Edge weight label
        mid_x = (x1 + x2) / 2.0
        mid_y = (y1 + y2) / 2.0
        ax.text(mid_x, mid_y + 0.15, f"{w}m", color=color, fontsize=9, fontweight='bold' if in_tree else 'normal',
                ha='center', bbox=dict(boxstyle='round,pad=0.15', facecolor='white', edgecolor='none', alpha=0.85))

    # Draw nodes
    for name, (x, y) in nodes.items():
        is_source = "Central" in name
        box_color = '#e3f2fd' if not is_source else '#ffebee'
        border_color = '#1565c0' if not is_source else '#c62828'
        ax.scatter(x, y, s=500, color=border_color, zorder=4)
        ax.text(x, y, name, ha='center', va='center', fontsize=8.5, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.35', facecolor=box_color, edgecolor=border_color, linewidth=1.5), zorder=5)

    ax.set_title('Figure 2.5: Metropolitan Transit Network & Bellman-Ford Optimal Delivery Tree (Red)', fontsize=12)
    ax.axis('off')
    ax.set_xlim(-3.5, 6.5)
    ax.set_ylim(-4.8, 5.2)

    import matplotlib.lines as mlines
    red_line = mlines.Line2D([], [], color='#d62728', lw=2.2, label='Optimal Shortest Route (Bellman-Ford DP)')
    gray_line = mlines.Line2D([], [], color='#9e9e9e', lw=1.2, ls='--', label='Alternative Road Corridor')
    ax.legend(handles=[red_line, gray_line], loc='lower right', frameon=True)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, "fig_city_routing_graph.png")
    fig.savefig(path, dpi=300)
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    generate_mergesort_chart()
    generate_closest_pair_chart()
    generate_knapsack_comparison_chart()
    generate_activity_schedule_chart()
    generate_city_routing_graph()
    print("All report figures generated successfully.")
