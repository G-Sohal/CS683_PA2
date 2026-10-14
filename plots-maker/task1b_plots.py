"""
CS683 PA2 — Task 1B: Prefetcher Evaluation

Compare Baseline, IP-stride, and SPP across traces.

Metrics:
    1. IPC
    2. Speedup
    3. L1D Load MPKI
    4. Prefetch Accuracy
    5. Prefetch Coverage

Run:
    python task1b_plots.py

Output:
    task1b_plots/
"""

import os
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. MANUAL DATA INPUT
# ============================================================

# Add or remove trace names here.
# Every metric array must have exactly len(TRACES) values.
TRACES = ["Trace 1", "Trace 2", "Trace 3"]

# Enter values in the same order as TRACES.
#
# speedup = IPC(policy) / IPC(Baseline)
# Baseline speedup is normally 1.0.
#
# Replace every None with your measured values.
# Keep accuracy and coverage in the same format throughout:
# either fractions (e.g. 0.75) or percentages (e.g. 75.0).
#
# Source: champsim/results/final/*.txt (25M warmup + 25M sim instructions,
# run from traces/ so the seed matches the Task 2 runs).
# accuracy (%) = L1D useful prefetches / prefetches issued to lower level
# coverage (%) = (baseline L1D load misses - L1D load misses) / baseline L1D load misses
# Baseline issues no prefetches, so its accuracy and coverage are 0.

DATA = {
    "Baseline": {
        "ipc":              [0.232288, 0.250638, 0.382008],
        "speedup":          [1.0, 1.0, 1.0],
        "l1d_load_mpki":    [10.6782, 13.5363, 3.40324],
        "accuracy":         [0.0, 0.0, 0.0],
        "coverage":         [0.0, 0.0, 0.0],
    },

    "IP-stride": {
        "ipc":              [0.233344, 0.250518, 0.382889],
        "speedup":          [1.0045, 0.9995, 1.0023],
        "l1d_load_mpki":    [10.1173, 13.4378, 3.31884],
        "accuracy":         [53.0, 38.17, 15.95],
        "coverage":         [5.25, 0.73, 2.48],
    },

    "SPP": {
        "ipc":              [0.233928, 0.251841, 0.388507],
        "speedup":          [1.0071, 1.0048, 1.017],
        "l1d_load_mpki":    [9.68772, 13.2022, 2.916],
        "accuracy":         [53.63, 46.27, 44.76],
        "coverage":         [9.28, 2.47, 14.32],
    },
}

# ============================================================
# 2. CONFIGURATION
# ============================================================

OUTPUT_DIR = "task1b_plots"
POLICIES = list(DATA.keys())

METRICS = [
    "ipc",
    "speedup",
    "l1d_load_mpki",
    "accuracy",
    "coverage",
]

# ============================================================
# 3. VALIDATE DATA
# ============================================================

def validate_data():
    """Check that all metric arrays are complete and correctly sized."""
    if not TRACES:
        raise ValueError("Add at least one trace to TRACES.")

    for policy, metrics in DATA.items():
        for metric in METRICS:
            values = metrics[metric]

            if len(values) != len(TRACES):
                raise ValueError(
                    f"{policy} / {metric}: expected {len(TRACES)} values, "
                    f"but got {len(values)}."
                )

            for i, value in enumerate(values):
                if value is None:
                    raise ValueError(
                        f"Missing {metric} for {policy} / {TRACES[i]}."
                    )

                if not isinstance(value, (int, float)):
                    raise ValueError(
                        f"{policy} / {metric} / {TRACES[i]} "
                        "must be numeric."
                    )


# ============================================================
# 4. GENERIC PLOTTING FUNCTION
# ============================================================

def plot_metric(metric, title, ylabel, filename, reference=None):
    """Create a grouped bar chart for the selected metric."""
    x = np.arange(len(TRACES))
    width = 0.8 / len(POLICIES)

    fig, ax = plt.subplots(
        figsize=(max(9, len(TRACES) * 1.5), 5.5)
    )

    for i, policy in enumerate(POLICIES):
        values = DATA[policy][metric]
        offset = (i - (len(POLICIES) - 1) / 2) * width

        bars = ax.bar(
            x + offset,
            values,
            width,
            label=policy,
        )

        ax.bar_label(bars, fmt="%.3g", padding=3, fontsize=8)

    if reference is not None:
        ax.axhline(
            reference,
            linestyle="--",
            linewidth=1.2,
            label=f"Reference = {reference}",
        )

    ax.set_title(title)
    ax.set_xlabel("Benchmark / Trace")
    ax.set_ylabel(ylabel)
    ax.set_xticks(x)
    ax.set_xticklabels(TRACES, rotation=20, ha="right")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    fig.tight_layout()

    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {filepath}")


# ============================================================
# 5. PRINT RESULTS TABLE
# ============================================================

def print_results():
    """Print all entered metrics in the terminal."""
    print("\nTASK 1B RESULTS")
    print("-" * 105)

    print(
        f"{'Trace':<14} {'Policy':<14} {'IPC':>9} "
        f"{'Speedup':>9} {'L1D MPKI':>11} "
        f"{'Accuracy':>11} {'Coverage':>11}"
    )

    print("-" * 105)

    for i, trace in enumerate(TRACES):
        for policy in POLICIES:
            row = DATA[policy]

            print(
                f"{trace:<14} {policy:<14} "
                f"{row['ipc'][i]:>9.4f} "
                f"{row['speedup'][i]:>9.4f} "
                f"{row['l1d_load_mpki'][i]:>11.4f} "
                f"{row['accuracy'][i]:>11.4f} "
                f"{row['coverage'][i]:>11.4f}"
            )

    print("-" * 105)


# ============================================================
# 6. MAIN: GENERATE ALL REQUIRED PLOTS
# ============================================================

def main():
    validate_data()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Plot 1: IPC.
    plot_metric(
        "ipc",
        "IPC Comparison: Baseline vs Prefetchers",
        "Instructions Per Cycle (IPC)",
        "task1b_ipc.png",
    )

    # Plot 2: Speedup over baseline.
    plot_metric(
        "speedup",
        "Speedup over Baseline",
        "Speedup",
        "task1b_speedup.png",
        reference=1.0,
    )

    # Plot 3: L1 Data-cache Load MPKI.
    plot_metric(
        "l1d_load_mpki",
        "L1D Load MPKI Comparison",
        "L1D Load MPKI",
        "task1b_l1d_load_mpki.png",
    )

    # Plot 4: Prefetch accuracy.
    plot_metric(
        "accuracy",
        "Prefetch Accuracy Comparison",
        "Prefetch Accuracy",
        "task1b_prefetch_accuracy.png",
    )

    # Plot 5: Prefetch coverage.
    plot_metric(
        "coverage",
        "Prefetch Coverage Comparison",
        "Prefetch Coverage",
        "task1b_prefetch_coverage.png",
    )

    print_results()
    print(f"\nAll plots saved in: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()