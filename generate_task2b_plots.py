import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('plots/task2b', exist_ok=True)

thresholds = [0.15, 0.20, 0.25, 0.30, 0.35]

# Data from Task 2b simulation runs
speedup = {
    'Trace 1': [1.0156, 1.0149, 1.0143, 1.0148, 1.0066],
    'Trace 2': [1.0357, 1.0349, 1.0350, 1.0338, 1.0336],
    'Trace 3': [1.0013, 1.0010, 1.0008, 1.0010, 1.0013]
}

instr_mpki = {
    'Trace 1': [9.0097, 9.0107, 9.0335, 9.0256, 9.4235],
    'Trace 2': [9.5434, 9.6674, 9.7580, 9.8976, 10.0058],
    'Trace 3': [0.9049, 0.9478, 0.9802, 1.0208, 1.0441]
}

data_mpki = {
    'Trace 1': [9.9064, 9.9059, 9.9042, 9.9024, 9.2258],
    'Trace 2': [11.7321, 11.6799, 11.6536, 11.6334, 11.6141],
    'Trace 3': [3.1463, 3.1026, 3.0815, 3.0316, 3.0137]
}

# 1. Sensitivity Plot: Speedup vs Threshold
plt.figure(figsize=(8, 5))
plt.plot(thresholds, speedup['Trace 1'], marker='o', linewidth=2, label='Trace 1', color='#4C72B0')
plt.plot(thresholds, speedup['Trace 2'], marker='s', linewidth=2, label='Trace 2', color='#55A868')
plt.plot(thresholds, speedup['Trace 3'], marker='^', linewidth=2, label='Trace 3', color='#C44E52')
plt.axhline(1.0, color='gray', linestyle='--', linewidth=1, label='Baseline')
plt.xlabel('Decision Threshold (θ)', fontsize=12)
plt.ylabel('Speedup over Baseline', fontsize=12)
plt.title('Dynamic I-RRIP: Speedup vs Threshold (Sensitivity Study)', fontsize=13, fontweight='bold')
plt.xticks(thresholds)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_speedup_sensitivity.png', dpi=300)
plt.close()

# 2. Sensitivity Plot: L2 Instruction MPKI vs Threshold
plt.figure(figsize=(8, 5))
plt.plot(thresholds, instr_mpki['Trace 1'], marker='o', linewidth=2, label='Trace 1', color='#4C72B0')
plt.plot(thresholds, instr_mpki['Trace 2'], marker='s', linewidth=2, label='Trace 2', color='#55A868')
plt.plot(thresholds, instr_mpki['Trace 3'], marker='^', linewidth=2, label='Trace 3', color='#C44E52')
plt.xlabel('Decision Threshold (θ)', fontsize=12)
plt.ylabel('L2 Instruction Load MPKI', fontsize=12)
plt.title('Dynamic I-RRIP: L2 Instruction MPKI vs Threshold', fontsize=13, fontweight='bold')
plt.xticks(thresholds)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_instr_mpki_sensitivity.png', dpi=300)
plt.close()

# 3. Sensitivity Plot: L2 Data MPKI vs Threshold
plt.figure(figsize=(8, 5))
plt.plot(thresholds, data_mpki['Trace 1'], marker='o', linewidth=2, label='Trace 1', color='#4C72B0')
plt.plot(thresholds, data_mpki['Trace 2'], marker='s', linewidth=2, label='Trace 2', color='#55A868')
plt.plot(thresholds, data_mpki['Trace 3'], marker='^', linewidth=2, label='Trace 3', color='#C44E52')
plt.xlabel('Decision Threshold (θ)', fontsize=12)
plt.ylabel('L2 Data Load MPKI', fontsize=12)
plt.title('Dynamic I-RRIP: L2 Data MPKI vs Threshold', fontsize=13, fontweight='bold')
plt.xticks(thresholds)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_data_mpki_sensitivity.png', dpi=300)
plt.close()

# 4. Comparative Bar Chart: Baseline vs RRIP vs Static I-RRIP vs Dynamic I-RRIP (θ=0.25)
traces_list = ['Trace 1', 'Trace 2', 'Trace 3']
x = np.arange(len(traces_list))
width = 0.2

ipc_compare = {
    'Baseline (LRU)': [0.2323, 0.2506, 0.3820],
    'RRIP':           [0.2323, 0.2513, 0.3816],
    'Static I-RRIP':  [0.2357, 0.2603, 0.3844],
    'Dynamic I-RRIP (θ=0.25)': [0.2356, 0.2594, 0.3823]
}

plt.figure(figsize=(9, 5))
plt.bar(x - 1.5*width, ipc_compare['Baseline (LRU)'], width, label='Baseline (LRU)', color='#4C72B0')
plt.bar(x - 0.5*width, ipc_compare['RRIP'],           width, label='RRIP',           color='#55A868')
plt.bar(x + 0.5*width, ipc_compare['Static I-RRIP'],  width, label='Static I-RRIP',  color='#C44E52')
plt.bar(x + 1.5*width, ipc_compare['Dynamic I-RRIP (θ=0.25)'], width, label='Dynamic I-RRIP (θ=0.25)', color='#8172B2')

plt.ylabel('IPC', fontsize=12)
plt.title('IPC Comparison: Baseline vs RRIP vs Static vs Dynamic I-RRIP', fontsize=13, fontweight='bold')
plt.xticks(x, traces_list, fontsize=11)
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2b/task2b_policy_comparison.png', dpi=300)
plt.close()

print("Task 2B plots successfully generated in plots/task2b/")
