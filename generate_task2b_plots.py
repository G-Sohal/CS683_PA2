import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('plots/task2b', exist_ok=True)

thresholds = [0.15, 0.20, 0.25, 0.30, 0.35]
traces = ['Trace 1', 'Trace 2', 'Trace 3']

# ---------------------------------------------------------
# Sensitivity Study Data (across 5 thresholds)
# ---------------------------------------------------------
ipc_sens = {
    'Trace 1': [0.2359, 0.2358, 0.2356, 0.2357, 0.2338],
    'Trace 2': [0.2596, 0.2594, 0.2594, 0.2591, 0.2590],
    'Trace 3': [0.3825, 0.3824, 0.3823, 0.3824, 0.3825]
}

speedup_sens = {
    'Trace 1': [1.0156, 1.0149, 1.0143, 1.0148, 1.0066],
    'Trace 2': [1.0357, 1.0349, 1.0350, 1.0338, 1.0336],
    'Trace 3': [1.0013, 1.0010, 1.0008, 1.0010, 1.0013]
}

l2c_mpki_sens = {
    'Trace 1': [18.9161, 18.9166, 18.9378, 18.9280, 18.6493],
    'Trace 2': [21.2755, 21.3472, 21.4116, 21.5311, 21.6199],
    'Trace 3': [4.0512,  4.0504,  4.0617,  4.0524,  4.0578]
}

instr_mpki_sens = {
    'Trace 1': [9.0097, 9.0107, 9.0335, 9.0256, 9.4235],
    'Trace 2': [9.5434, 9.6674, 9.7580, 9.8976, 10.0058],
    'Trace 3': [0.9049, 0.9478, 0.9802, 1.0208, 1.0441]
}

data_mpki_sens = {
    'Trace 1': [9.9064,  9.9059,  9.9042,  9.9024,  9.2258],
    'Trace 2': [11.7321, 11.6799, 11.6536, 11.6334, 11.6141],
    'Trace 3': [3.1463,  3.1026,  3.0815,  3.0316,  3.0137]
}

# 1. Sensitivity Plot: IPC vs Threshold
plt.figure(figsize=(8, 5))
plt.plot(thresholds, ipc_sens['Trace 1'], marker='o', linewidth=2, label='Trace 1', color='#4C72B0')
plt.plot(thresholds, ipc_sens['Trace 2'], marker='s', linewidth=2, label='Trace 2', color='#55A868')
plt.plot(thresholds, ipc_sens['Trace 3'], marker='^', linewidth=2, label='Trace 3', color='#C44E52')
plt.xlabel('Decision Threshold (θ)', fontsize=12)
plt.ylabel('Instructions Per Cycle (IPC)', fontsize=12)
plt.title('Dynamic I-RRIP: IPC vs Decision Threshold (θ)', fontsize=13, fontweight='bold')
plt.xticks(thresholds)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_ipc_sensitivity.png', dpi=300)
plt.close()

# 2. Sensitivity Plot: Speedup vs Threshold
plt.figure(figsize=(8, 5))
plt.plot(thresholds, speedup_sens['Trace 1'], marker='o', linewidth=2, label='Trace 1', color='#4C72B0')
plt.plot(thresholds, speedup_sens['Trace 2'], marker='s', linewidth=2, label='Trace 2', color='#55A868')
plt.plot(thresholds, speedup_sens['Trace 3'], marker='^', linewidth=2, label='Trace 3', color='#C44E52')
plt.axhline(1.0, color='gray', linestyle='--', linewidth=1, label='Baseline')
plt.xlabel('Decision Threshold (θ)', fontsize=12)
plt.ylabel('Speedup over Baseline', fontsize=12)
plt.title('Dynamic I-RRIP: Speedup vs Decision Threshold (θ)', fontsize=13, fontweight='bold')
plt.xticks(thresholds)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_speedup_sensitivity.png', dpi=300)
plt.close()

# 3. Sensitivity Plot: 3-Panel MPKI Sensitivity vs Threshold
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

for tr, col, mark in zip(traces, ['#4C72B0', '#55A868', '#C44E52'], ['o', 's', '^']):
    axes[0].plot(thresholds, l2c_mpki_sens[tr], marker=mark, linewidth=2, label=tr, color=col)
    axes[1].plot(thresholds, instr_mpki_sens[tr], marker=mark, linewidth=2, label=tr, color=col)
    axes[2].plot(thresholds, data_mpki_sens[tr], marker=mark, linewidth=2, label=tr, color=col)

axes[0].set_title('(a) Total L2C Load MPKI', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Decision Threshold (θ)', fontsize=11)
axes[0].set_ylabel('Total L2C MPKI', fontsize=11)
axes[0].set_xticks(thresholds)
axes[0].grid(True, linestyle=':', alpha=0.7)
axes[0].legend(frameon=True, fontsize=9)

axes[1].set_title('(b) L2 Instruction Load MPKI', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Decision Threshold (θ)', fontsize=11)
axes[1].set_ylabel('L2 Instruction MPKI', fontsize=11)
axes[1].set_xticks(thresholds)
axes[1].grid(True, linestyle=':', alpha=0.7)
axes[1].legend(frameon=True, fontsize=9)

axes[2].set_title('(c) L2 Data Load MPKI', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Decision Threshold (θ)', fontsize=11)
axes[2].set_ylabel('L2 Data MPKI', fontsize=11)
axes[2].set_xticks(thresholds)
axes[2].grid(True, linestyle=':', alpha=0.7)
axes[2].legend(frameon=True, fontsize=9)

plt.suptitle('Dynamic I-RRIP: Load MPKI Sensitivity vs Decision Threshold (θ)', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_mpki_sensitivity.png', dpi=300, bbox_inches='tight')
plt.close()

# ---------------------------------------------------------
# Policy Comparison Data (Consistent 4 Configurations)
# Baseline (LRU), RRIP, Static I-RRIP, Dynamic I-RRIP (θ=0.25)
# ---------------------------------------------------------
x = np.arange(len(traces))
width = 0.2
colors4 = ['#4C72B0', '#55A868', '#C44E52', '#8172B2']
labels4 = ['Baseline (LRU)', 'RRIP', 'Static I-RRIP', 'Dynamic I-RRIP (θ=0.25)']

ipc_all = {
    'Baseline (LRU)': [0.2323, 0.2506, 0.3820],
    'RRIP':           [0.2323, 0.2513, 0.3816],
    'Static I-RRIP':  [0.2357, 0.2603, 0.3844],
    'Dynamic I-RRIP (θ=0.25)': [0.2356, 0.2594, 0.3823]
}

speedup_all = {
    'Baseline (LRU)': [1.0000, 1.0000, 1.0000],
    'RRIP':           [0.2323/0.2323, 0.2513/0.2506, 0.3816/0.3820],
    'Static I-RRIP':  [0.2357/0.2323, 0.2603/0.2506, 0.3844/0.3820],
    'Dynamic I-RRIP (θ=0.25)': [0.2356/0.2323, 0.2594/0.2506, 0.3823/0.3820]
}

l2c_mpki_all = {
    'Baseline (LRU)': [17.7509, 28.2286, 3.9592],
    'RRIP':           [17.6814, 26.6066, 4.0443],
    'Static I-RRIP':  [19.0249, 21.6864, 3.9884],
    'Dynamic I-RRIP (θ=0.25)': [18.9378, 21.4116, 4.0617]
}

instr_mpki_all = {
    'Baseline (LRU)': [10.4030, 19.5298, 1.1232],
    'RRIP':           [10.6129, 18.5456, 1.1976],
    'Static I-RRIP':  [9.0044,   9.2780, 0.7153],
    'Dynamic I-RRIP (θ=0.25)': [9.0335,  9.7580, 0.9802]
}

data_mpki_all = {
    'Baseline (LRU)': [7.3479,  8.6988,  2.8360],
    'RRIP':           [7.0684,  8.0610,  2.8467],
    'Static I-RRIP':  [10.0204, 12.4084, 3.2731],
    'Dynamic I-RRIP (θ=0.25)': [9.9042, 11.6536, 3.0815]
}

# 4. Comparative Bar Chart: IPC
plt.figure(figsize=(9, 5))
for i, (lab, col) in enumerate(zip(labels4, colors4)):
    offset = (i - 1.5) * width
    plt.bar(x + offset, ipc_all[lab], width, label=lab, color=col)

plt.ylabel('Instructions Per Cycle (IPC)', fontsize=12)
plt.title('Performance Comparison: IPC across L2 Replacement Policies', fontsize=13, fontweight='bold')
plt.xticks(x, traces, fontsize=11)
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_ipc_comparison.png', dpi=300)
plt.close()

# 5. Comparative Bar Chart: Speedup
plt.figure(figsize=(9, 5))
for i, (lab, col) in enumerate(zip(labels4, colors4)):
    offset = (i - 1.5) * width
    plt.bar(x + offset, speedup_all[lab], width, label=lab, color=col)

plt.axhline(1.0, color='gray', linestyle='--', linewidth=1)
plt.ylabel('Speedup over Baseline', fontsize=12)
plt.title('Performance Comparison: Speedup across L2 Replacement Policies', fontsize=13, fontweight='bold')
plt.xticks(x, traces, fontsize=11)
plt.ylim(0.95, 1.06)
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_speedup_comparison.png', dpi=300)
plt.close()

# 6. Combined 3-Panel MPKI Policy Comparison
fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

for i, (lab, col) in enumerate(zip(labels4, colors4)):
    offset = (i - 1.5) * width
    axes[0].bar(x + offset, l2c_mpki_all[lab],   width, label=lab, color=col)
    axes[1].bar(x + offset, instr_mpki_all[lab], width, label=lab, color=col)
    axes[2].bar(x + offset, data_mpki_all[lab],  width, label=lab, color=col)

axes[0].set_title('(a) Total L2C Load MPKI', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Load MPKI', fontsize=11)
axes[0].set_xticks(x)
axes[0].set_xticklabels(traces, fontsize=10)
axes[0].grid(axis='y', linestyle=':', alpha=0.7)
axes[0].legend(frameon=True, fontsize=8.5)

axes[1].set_title('(b) L2 Instruction Load MPKI', fontsize=12, fontweight='bold')
axes[1].set_xticks(x)
axes[1].set_xticklabels(traces, fontsize=10)
axes[1].grid(axis='y', linestyle=':', alpha=0.7)
axes[1].legend(frameon=True, fontsize=8.5)

axes[2].set_title('(c) L2 Data Load MPKI', fontsize=12, fontweight='bold')
axes[2].set_xticks(x)
axes[2].set_xticklabels(traces, fontsize=10)
axes[2].grid(axis='y', linestyle=':', alpha=0.7)
axes[2].legend(frameon=True, fontsize=8.5)

plt.suptitle('Task 2B: L2 Load MPKI Comparison across Configurations', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_mpki_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("Task 2B plots successfully generated in plots/task2b/")
