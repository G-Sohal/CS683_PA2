"""
CS683 PA2 — Task 3: Combined Prefetching and Cache Replacement

Metrics:
    IPC, Speedup, Prefetch Accuracy, Prefetch Coverage,
    L1D Load MPKI, L2C Load MPKI, L2 Instruction MPKI,
    L2 Data MPKI.

Run:
    python task3_plots.py
"""

import os
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. MANUALLY ENTER DATA
# ============================================================

TRACES = ["Trace 1", "Trace 2", "Trace 3"]

# Replace None with your measured values.
# Every array must follow the same order as TRACES.
# Use one consistent format for accuracy and coverage:
# fractions (0–1) OR percentages (0–100).

# Source: champsim/results/task3/*.txt (25M warmup + 25M sim instructions).
# accuracy (%) = L1D useful prefetches / prefetches issued to lower level
# coverage (%) = (baseline L1D load misses - L1D load misses) / baseline L1D load misses
# Configurations without a prefetcher have accuracy and coverage 0.

DATA = {
    "Baseline": {
        "ipc":             [0.232113, 0.249982, 0.381868],
        "speedup":         [1.0, 1.0, 1.0],
        "accuracy":        [0.0, 0.0, 0.0],
        "coverage":        [0.0, 0.0, 0.0],
        "l1d_load_mpki":   [10.6788, 13.5372, 3.40356],
        "l2c_load_mpki":   [17.7251, 28.5496, 3.96124],
        "l2i_load_mpki":   [10.3665, 19.844, 1.12652],
        "l2d_load_mpki":   [7.35864, 8.7056, 2.83472],
    },

    "SPP": {
        "ipc":             [0.233796, 0.251126, 0.388273],
        "speedup":         [1.0073, 1.0046, 1.0168],
        "accuracy":        [53.48, 46.03, 44.96],
        "coverage":        [9.26, 2.45, 14.37],
        "l1d_load_mpki":   [9.69012, 13.2056, 2.91452],
        "l2c_load_mpki":   [16.9386, 28.4368, 3.32028],
        "l2i_load_mpki":   [10.42, 20.0366, 1.14348],
        "l2d_load_mpki":   [6.5186, 8.40016, 2.1768],
    },

    "Dynamic I-RRIP": {
        "ipc":             [0.232427, 0.255004, 0.381807],
        "speedup":         [1.0014, 1.0201, 0.9998],
        "accuracy":        [0.0, 0.0, 0.0],
        "coverage":        [0.0, 0.0, 0.0],
        "l1d_load_mpki":   [10.6789, 13.5413, 3.40368],
        "l2c_load_mpki":   [17.4772, 23.7324, 3.9112],
        "l2i_load_mpki":   [10.2429, 14.6092, 1.08976],
        "l2d_load_mpki":   [7.23432, 9.12316, 2.82144],
    },

    "SPP + Dynamic I-RRIP": {
        "ipc":             [0.234257, 0.256352, 0.388424],
        "speedup":         [1.0092, 1.0255, 1.0172],
        "accuracy":        [53.53, 45.34, 44.96],
        "coverage":        [9.26, 2.38, 14.45],
        "l1d_load_mpki":   [9.69016, 13.2157, 2.9116],
        "l2c_load_mpki":   [16.6096, 23.4646, 3.22784],
        "l2i_load_mpki":   [10.2223, 14.6674, 1.07924],
        "l2d_load_mpki":   [6.38728, 8.79716, 2.1486],
    }
}

# ============================================================
# 2. CONFIGURATION
# ============================================================

OUTPUT_DIR = "task3_plots"
POLICIES = list(DATA.keys())

METRICS = [
    "ipc",
    "speedup",
    "accuracy",
    "coverage",
    "l1d_load_mpki",
    "l2c_load_mpki",
    "l2i_load_mpki",
    "l2d_load_mpki",
]

# Accuracy and coverage are meaningful only for configurations
# that actually use a prefetcher. Edit this list if needed.
PREFETCH_POLICIES = [
    "SPP",
    "SPP + Dynamic I-RRIP",
]

# ============================================================
# 3. VALIDATION
# ============================================================

def validate_data():
    if not TRACES:
        raise ValueError("Add at least one trace.")

    for policy, metrics in DATA.items():
        for metric in METRICS:
            values = metrics[metric]

            if len(values) != len(TRACES):
                raise ValueError(
                    f"{policy}/{metric}: expected {len(TRACES)} values."
                )

            for i, value in enumerate(values):
                if value is None:
                    raise ValueError(
                        f"Missing {metric} for {policy}/{TRACES[i]}."
                    )

                if not isinstance(value, (int, float)):
                    raise ValueError(
                        f"{policy}/{metric}/{TRACES[i]} must be numeric."
                    )

# ============================================================
# 4. PLOTTING
# ============================================================

def plot_metric(metric, title, ylabel, filename,
                policies=None, reference=None):
    if policies is None:
        policies = POLICIES

    x = np.arange(len(TRACES))
    width = 0.8 / len(policies)

    fig, ax = plt.subplots(
        figsize=(max(9, len(TRACES) * 1.5), 5.5)
    )

    for i, policy in enumerate(policies):
        values = DATA[policy][metric]
        offset = (i - (len(policies) - 1) / 2) * width

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

    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {path}")

# ============================================================
# 5. RESULTS TABLE
# ============================================================

def print_results():
    print("\nTASK 3 RESULTS")
    print("=" * 125)

    for policy in POLICIES:
        print(f"\n{policy}")
        print(
            f"{'Trace':<14} {'IPC':>9} {'Speedup':>9} "
            f"{'Accuracy':>11} {'Coverage':>11} "
            f"{'L1D MPKI':>11} {'L2C MPKI':>11} "
            f"{'L2I MPKI':>11} {'L2D MPKI':>11}"
        )

        for i, trace in enumerate(TRACES):
            d = DATA[policy]
            print(
                f"{trace:<14} "
                f"{d['ipc'][i]:>9.4f} "
                f"{d['speedup'][i]:>9.4f} "
                f"{d['accuracy'][i]:>11.4f} "
                f"{d['coverage'][i]:>11.4f} "
                f"{d['l1d_load_mpki'][i]:>11.4f} "
                f"{d['l2c_load_mpki'][i]:>11.4f} "
                f"{d['l2i_load_mpki'][i]:>11.4f} "
                f"{d['l2d_load_mpki'][i]:>11.4f}"
            )

# ============================================================
# 6. MAIN
# ============================================================

def main():
    validate_data()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plot_metric(
        "ipc",
        "Task 3: IPC Comparison",
        "IPC",
        "task3_ipc.png",
    )

    plot_metric(
        "speedup",
        "Task 3: Speedup over Baseline",
        "Speedup",
        "task3_speedup.png",
        reference=1.0,
    )

    plot_metric(
        "accuracy",
        "Task 3: Prefetch Accuracy",
        "Prefetch Accuracy",
        "task3_accuracy.png",
        policies=PREFETCH_POLICIES,
    )

    plot_metric(
        "coverage",
        "Task 3: Prefetch Coverage",
        "Prefetch Coverage",
        "task3_coverage.png",
        policies=PREFETCH_POLICIES,
    )

    plot_metric(
        "l1d_load_mpki",
        "Task 3: L1D Load MPKI",
        "L1D Load MPKI",
        "task3_l1d_load_mpki.png",
    )

    plot_metric(
        "l2c_load_mpki",
        "Task 3: L2C Load MPKI",
        "L2C Load MPKI",
        "task3_l2c_load_mpki.png",
    )

    plot_metric(
        "l2i_load_mpki",
        "Task 3: L2 Instruction MPKI",
        "L2 Instruction MPKI",
        "task3_l2i_load_mpki.png",
    )

    plot_metric(
        "l2d_load_mpki",
        "Task 3: L2 Data MPKI",
        "L2 Data MPKI",
        "task3_l2d_load_mpki.png",
    )

    print_results()
    print(f"\nAll plots saved in '{OUTPUT_DIR}/'.")

if __name__ == "__main__":
    main()