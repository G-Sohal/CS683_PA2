"""
CS683 PA2 — Task 2A: I-RRIP

Enter your measured results in the DATA section.
All values are manually entered; this script does not run ChampSim.

Run:
    python task2a_plots.py

Output:
    task2a_plots/
"""

import os
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. MANUAL DATA INPUT
# ============================================================

# Add or remove traces here.
# Every metric array below must have exactly len(TRACES) values.
TRACES = ["Trace 1", "Trace 2", "Trace 3"]

# Enter results in the same order as TRACES.
# Example: [0.8, 1.1, 0.95] means:
# Trace 1 = 0.8, Trace 2 = 1.1, Trace 3 = 0.95.
#
# speedup = IPC of this policy / IPC of Baseline RRIP.
# Baseline speedup is normally 1.0.
#
# Replace all None values with your actual measurements.

DATA = {
    "Baseline RRIP": {
        "ipc":             [None, None, None],
        "speedup":         [1.0, 1.0, 1.0],
        "l2c_load_mpki":   [None, None, None],
        "l2i_load_mpki":   [None, None, None],
        "l2d_load_mpki":   [None, None, None],
    },

    "I-RRIP": {
        "ipc":             [None, None, None],
        "speedup":         [None, None, None],
        "l2c_load_mpki":   [None, None, None],
        "l2i_load_mpki":   [None, None, None],
        "l2d_load_mpki":   [None, None, None],
    },
}

# ============================================================
# 2. CONFIGURATION
# ============================================================

OUTPUT_DIR = "task2a_plots"
POLICIES = list(DATA.keys())

METRICS = [
    "ipc",
    "speedup",
    "l2c_load_mpki",
    "l2i_load_mpki",
    "l2d_load_mpki",
]

# ============================================================
# 3. VALIDATE DATA
# ============================================================

def validate_data():
    """Check array lengths and make sure no required values are missing."""
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
                        f"{metric} for {policy} / {TRACES[i]} "
                        "must be numeric."
                    )


# ============================================================
# 4. PLOTTING FUNCTION
# ============================================================

def plot_metric(metric, title, ylabel, filename, reference=None):
    """Plot a metric across traces for all configured policies."""
    x = np.arange(len(TRACES))
    width = 0.8 / len(POLICIES)

    fig, ax = plt.subplots(
        figsize=(max(9, len(TRACES) * 1.5), 5.5)
    )

    for i, policy in enumerate(POLICIES):
        values = DATA[policy][metric]
        offset = (i - (len(POLICIES) - 1) / 2) * width

        bars = ax.bar(
            x + offset, values, width, label=policy
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
# 5. PRINT RESULTS TABLE
# ============================================================

def print_results():
    """Print the entered values in the terminal."""
    print("\nTASK 2A RESULTS")
    print("-" * 105)
    print(
        f"{'Trace':<16} {'Policy':<18} {'IPC':>9} "
        f"{'Speedup':>9} {'L2C MPKI':>11} "
        f"{'L2I MPKI':>11} {'L2D MPKI':>11}"
    )
    print("-" * 105)

    for i, trace in enumerate(TRACES):
        for policy in POLICIES:
            print(
                f"{trace:<16} {policy:<18} "
                f"{DATA[policy]['ipc'][i]:>9.4f} "
                f"{DATA[policy]['speedup'][i]:>9.4f} "
                f"{DATA[policy]['l2c_load_mpki'][i]:>11.4f} "
                f"{DATA[policy]['l2i_load_mpki'][i]:>11.4f} "
                f"{DATA[policy]['l2d_load_mpki'][i]:>11.4f}"
            )

    print("-" * 105)


# ============================================================
# 6. MAIN: GENERATE ALL PLOTS
# ============================================================

def main():
    validate_data()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plot_metric(
        "ipc", "IPC: RRIP vs I-RRIP", "IPC",
        "task2a_ipc.png"
    )

    plot_metric(
        "speedup", "Speedup over Baseline RRIP", "Speedup",
        "task2a_speedup.png", reference=1.0
    )

    plot_metric(
        "l2c_load_mpki", "L2C Load MPKI",
        "L2C Load MPKI", "task2a_l2c_load_mpki.png"
    )

    plot_metric(
        "l2i_load_mpki", "L2 Instruction Load MPKI",
        "L2 Instruction Load MPKI",
        "task2a_l2_instruction_load_mpki.png"
    )

    plot_metric(
        "l2d_load_mpki", "L2 Data Load MPKI",
        "L2 Data Load MPKI", "task2a_l2_data_load_mpki.png"
    )

    print_results()
    print(f"\nAll plots saved in: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()