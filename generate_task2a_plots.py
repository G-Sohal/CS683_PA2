import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('plots/task2a', exist_ok=True)

traces = ['Trace 1', 'Trace 2', 'Trace 3']

# Data extracted from simulation results
ipc = {
    'Baseline (LRU)': [0.2323, 0.2506, 0.3820],
    'RRIP':           [0.2323, 0.2513, 0.3816],
    'I-RRIP':         [0.2357, 0.2603, 0.3844]
}

speedup = {
    'Baseline (LRU)': [1.0000, 1.0000, 1.0000],
    'RRIP':           [0.2323/0.2323, 0.2513/0.2506, 0.3816/0.3820],
    'I-RRIP':         [0.2357/0.2323, 0.2603/0.2506, 0.3844/0.3820]
}

l2c_load_mpki = {
    'Baseline (LRU)': [17.7509, 28.2286, 3.9592],
    'RRIP':           [17.6814, 26.6066, 4.0443],
    'I-RRIP':         [19.0249, 21.6864, 3.9884]
}

l2_instr_mpki = {
    'Baseline (LRU)': [10.4030, 19.5298, 1.1232],
    'RRIP':           [10.6129, 18.5456, 1.1976],
    'I-RRIP':         [9.0044,   9.2780, 0.7153]
}

l2_data_mpki = {
    'Baseline (LRU)': [7.3479, 8.6988, 2.8360],
    'RRIP':           [7.0684, 8.0610, 2.8467],
    'I-RRIP':         [10.0204, 12.4084, 3.2731]
}

x = np.arange(len(traces))
width = 0.25

# 1. Speedup Plot
plt.figure(figsize=(8, 5))
plt.bar(x - width, speedup['Baseline (LRU)'], width, label='Baseline (LRU)', color='#4C72B0')
plt.bar(x,         speedup['RRIP'],           width, label='RRIP',           color='#55A868')
plt.bar(x + width, speedup['I-RRIP'],         width, label='I-RRIP',         color='#C44E52')

plt.axhline(1.0, color='grey', linestyle='--', linewidth=1)
plt.ylabel('Speedup over Baseline', fontsize=12)
plt.title('Speedup of L2 Replacement Policies over Baseline', fontsize=14, fontweight='bold')
plt.xticks(x, traces, fontsize=11)
plt.ylim(0.95, 1.06)
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2a/task2a_speedup.png', dpi=300)
plt.close()

# 2. L2 Instruction Load MPKI Plot
plt.figure(figsize=(8, 5))
plt.bar(x - width, l2_instr_mpki['Baseline (LRU)'], width, label='Baseline (LRU)', color='#4C72B0')
plt.bar(x,         l2_instr_mpki['RRIP'],           width, label='RRIP',           color='#55A868')
plt.bar(x + width, l2_instr_mpki['I-RRIP'],         width, label='I-RRIP',         color='#C44E52')

plt.ylabel('L2 Instruction Load MPKI', fontsize=12)
plt.title('L2 Instruction Load MPKI Comparison', fontsize=14, fontweight='bold')
plt.xticks(x, traces, fontsize=11)
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2a/task2a_instr_mpki.png', dpi=300)
plt.close()

# 3. L2 Data Load MPKI Plot
plt.figure(figsize=(8, 5))
plt.bar(x - width, l2_data_mpki['Baseline (LRU)'], width, label='Baseline (LRU)', color='#4C72B0')
plt.bar(x,         l2_data_mpki['RRIP'],           width, label='RRIP',           color='#55A868')
plt.bar(x + width, l2_data_mpki['I-RRIP'],         width, label='I-RRIP',         color='#C44E52')

plt.ylabel('L2 Data Load MPKI', fontsize=12)
plt.title('L2 Data Load MPKI Comparison', fontsize=14, fontweight='bold')
plt.xticks(x, traces, fontsize=11)
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2a/task2a_data_mpki.png', dpi=300)
plt.close()

# 4. Total L2C Load MPKI Plot
plt.figure(figsize=(8, 5))
plt.bar(x - width, l2c_load_mpki['Baseline (LRU)'], width, label='Baseline (LRU)', color='#4C72B0')
plt.bar(x,         l2c_load_mpki['RRIP'],           width, label='RRIP',           color='#55A868')
plt.bar(x + width, l2c_load_mpki['I-RRIP'],         width, label='I-RRIP',         color='#C44E52')

plt.ylabel('L2C Total Load MPKI', fontsize=12)
plt.title('L2C Total Load MPKI Comparison', fontsize=14, fontweight='bold')
plt.xticks(x, traces, fontsize=11)
plt.grid(axis='y', linestyle=':', alpha=0.7)
plt.legend(frameon=True, fontsize=10)
plt.tight_layout()
plt.savefig('plots/task2a/task2a_total_l2c_mpki.png', dpi=300)
plt.close()

print("Plots successfully generated in plots/task2a/")
