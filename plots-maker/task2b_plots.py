"""
CS683 PA2 — Task 2B: Dynamic I-RRIP Sensitivity Analysis

Enter your measured results manually in DATA.
Each configuration has one value per trace.

Run:
    python task2b_plots.py

Output:
    task2b_plots/
"""

import os
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. MANUAL DATA INPUT
# ============================================================

# Every array must contain exactly len(TRACES) values.
TRACES = ["Trace 1", "Trace 2", "Trace 3"]

# Replace the configuration labels with your actual thresholds.
# For example, use "Threshold = 4" if that is what you tested.
#
# Enter the IPC and all three L2 MPKI metrics for every configuration.
# Speedup = IPC(configuration) / IPC(baseline RRIP).
#
# Replace every None with your measured result.

DATA = {
    "Baseline RRIP": {
        "ipc":             [None, None, None],
        "speedup":         [1.0, 1.0, 1.0],
        "l2c_load_mpki":   [None, None, None],
        "l2i_load_mpki":   [None, None, None],
        "l2d_load_mpki":   [None, None, None],
    },

    "Threshold 1": {
        "ipc":             [None, None, None],
        "speedup":         [None, None, None],
        "l2c_load_mpki":   [None, None, None],
        "l2i_load_mpki":   [None, None, None],
        "l2d_load_mpki":   [None, None, None],
    },

    "Threshold 2": {
        "ipc":             [None, None, None],
        "speedup":         [None, None, None],
        "l2c_load_mpki":   [None, None, None],
        "l2i_load_mpki":   [None, None, None],
        "l2d_load_mpki":   [None, None, None],
    },

    "Threshold 3": {
        "ipc":             [None, None, None],
        "speedup":         [None, None, None],
        "l2c_load_mpki":   [None, None, None],
        "l2i_load_mpki":   [None, None, None],
        "l2d_load_mpki":   [None, None, None],
    },

    "Threshold 4": {
        "ipc":             [None, None, None],
        "speedup":         [None, None, None],
        "l2c_load_mpki":   [None, None, None],
        "l2i_load_mpki":   [None, None, None],
        "l2d_load_mpki":   [None, None, None],
    },

    "Threshold 5": {
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

OUTPUT_DIR = "task2b_plots"
BASELINE = "Baseline RRIP"
CONFIGURATIONS = list(DATA.keys())

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
    """Validate that all arrays are complete and have matching lengths."""
    if not TRACES:
        raise ValueError("Add at least one trace to TRACES.")

    if BASELINE not in DATA:
        raise ValueError(f"DATA must contain {BASELINE!r}.")

    for config, metrics in DATA.items():
        for metric in METRICS:
            values = metrics[metric]

            if len(values) != len(TRACES):
                raise ValueError(
                    f"{config} / {metric}: expected {len(TRACES)} values, "
                    f"but got {len(values)}."
                )

            for i, value in enumerate(values):
                if value is None:
                    raise ValueError(
                        f"Missing {metric} for {config} / {TRACES[i]}."
                    )

                if not isinstance(value, (int, float)):
                    raise ValueError(
                        f"{config} / {metric} / {TRACES[i]} "
                        "must be numeric."
                    )


# ============================================================
# 4. GENERIC PLOTTING FUNCTION
# ============================================================

def plot_metric(metric, title, ylabel, filename, configs=None,
                reference=None):
    """Generate a grouped bar chart for the selected configurations."""
    if configs is None:
        configs = CONFIGURATIONS

    x = np.arange(len(TRACES))
    width = 0.8 / len(configs)

    fig, ax = plt.subplots(
        figsize=(max(10, len(TRACES) * 1.5), 6)
    )

    for i, config in enumerate(configs):
        values = DATA[config][metric]
        offset = (i - (len(configs) - 1) / 2) * width

        bars = ax.bar(
            x + offset, values, width, label=config
        )
        ax.bar_label(bars, fmt="%.3g", padding=3, fontsize=7)

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
    ax.legend(fontsize="small")
    ax.grid(axis="y", alpha=0.3)
    ax.set_axisbelow(True)

    fig.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {path}")


# ============================================================
# 5. THRESHOLD SENSITIVITY PLOT
# ============================================================

def plot_threshold_sensitivity():
    """
    Compare speedup across threshold settings.

    The baseline is excluded from the bars because it is the reference.
    The horizontal line at 1.0 represents baseline performance.
    """
    threshold_configs = [
        config for config in CONFIGURATIONS if config != BASELINE
    ]

    plot_metric(
        "speedup",
        "Threshold Sensitivity: Speedup over Baseline",
        "Speedup",
        "task2b_threshold_sensitivity.png",
        configs=threshold_configs,
        reference=1.0,
    )


# ============================================================
# 6. PRINT RESULTS TABLE
# ============================================================

def print_results():
    """Print the manually entered data for easy report preparation."""
    print("\nTASK 2B RESULTS")
    print("-" * 115)
    print(
        f"{'Trace':<14} {'Configuration':<22} {'IPC':>9} "
        f"{'Speedup':>9} {'L2C MPKI':>11} "
        f"{'L2I MPKI':>11} {'L2D MPKI':>11}"
    )
    print("-" * 115)

    for i, trace in enumerate(TRACES):
        for config in CONFIGURATIONS:
            r = DATA[config]
            print(
                f"{trace:<14} {config:<22} "
                f"{r['ipc'][i]:>9.4f} "
                f"{r['speedup'][i]:>9.4f} "
                f"{r['l2c_load_mpki'][i]:>11.4f} "
                f"{r['l2i_load_mpki'][i]:>11.4f} "
                f"{r['l2d_load_mpki'][i]:>11.4f}"
            )

    print("-" * 115)


# ============================================================
# 7. MAIN: GENERATE ALL PLOTS
# ============================================================

def main():
    validate_data()
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    plot_metric(
        "ipc", "IPC Across Threshold Settings", "IPC",
        "task2b_ipc.png"
    )

    plot_metric(
        "speedup", "Speedup Across Configurations", "Speedup",
        "task2b_speedup.png", reference=1.0
    )

    plot_metric(
        "l2c_load_mpki", "L2C Load MPKI",
        "L2C Load MPKI", "task2b_l2c_load_mpki.png"
    )

    plot_metric(
        "l2i_load_mpki", "L2 Instruction Load MPKI",
        "L2 Instruction Load MPKI",
        "task2b_l2_instruction_load_mpki.png"
    )

    plot_metric(
        "l2d_load_mpki", "L2 Data Load MPKI",
        "L2 Data Load MPKI", "task2b_l2_data_load_mpki.png"
    )

    # Additional plot comparing only the threshold configurations.
    plot_threshold_sensitivity()

    print_results()
    print(f"\nAll plots saved in: {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()