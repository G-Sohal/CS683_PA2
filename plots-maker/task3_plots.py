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

# Source: champsim/results/final/*.txt (25M warmup + 25M sim instructions,
# run from traces/ so the seed matches the Task 2 runs).
# accuracy (%) = L1D useful prefetches / prefetches issued to lower level
# coverage (%) = (baseline L1D load misses - L1D load misses) / baseline L1D load misses
# Configurations without a prefetcher have accuracy and coverage 0.

DATA = {
    "Baseline": {
        "ipc":             [0.232288, 0.250638, 0.382008],
        "speedup":         [1.0, 1.0, 1.0],
        "accuracy":        [0.0, 0.0, 0.0],
        "coverage":        [0.0, 0.0, 0.0],
        "l1d_load_mpki":   [10.6782, 13.5363, 3.40324],
        "l2c_load_mpki":   [17.7509, 28.2286, 3.95916],
        "l2i_load_mpki":   [10.403, 19.5298, 1.12316],
        "l2d_load_mpki":   [7.34788, 8.6988, 2.836],
    },

    "SPP": {
        "ipc":             [0.233928, 0.251841, 0.388507],
        "speedup":         [1.0071, 1.0048, 1.017],
        "accuracy":        [53.63, 46.27, 44.76],
        "coverage":        [9.28, 2.47, 14.32],
        "l1d_load_mpki":   [9.68772, 13.2022, 2.916],
        "l2c_load_mpki":   [16.9328, 28.1228, 3.32016],
        "l2i_load_mpki":   [10.4213, 19.7253, 1.14056],
        "l2d_load_mpki":   [6.51148, 8.39748, 2.1796],
    },

    "Dynamic I-RRIP": {
        "ipc":             [0.235618, 0.259407, 0.382299],
        "speedup":         [1.0143, 1.035, 1.0008],
        "accuracy":        [0.0, 0.0, 0.0],
        "coverage":        [0.0, 0.0, 0.0],
        "l1d_load_mpki":   [10.6802, 13.5458, 3.4034],
        "l2c_load_mpki":   [18.9378, 21.4116, 4.06168],
        "l2i_load_mpki":   [9.03352, 9.75796, 0.98016],
        "l2d_load_mpki":   [9.90424, 11.6536, 3.08152],
    },

    "SPP + Dynamic I-RRIP": {
        "ipc":             [0.237936, 0.260965, 0.388846],
        "speedup":         [1.0243, 1.0412, 1.0179],
        "accuracy":        [53.17, 45.23, 45.32],
        "coverage":        [9.14, 2.31, 14.44],
        "l1d_load_mpki":   [9.70192, 13.223, 2.91184],
        "l2c_load_mpki":   [17.8633, 21.086, 3.40372],
        "l2i_load_mpki":   [9.03576, 9.72108, 0.98344],
        "l2d_load_mpki":   [8.82756, 11.365, 2.42028],
    },
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