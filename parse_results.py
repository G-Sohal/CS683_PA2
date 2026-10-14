import re
import os

traces = ['Trace1', 'Trace2', 'Trace3']
policies = ['baseline', 'rrip', 'irrip']

results = {}

for p in policies:
    results[p] = {}
    for t in traces:
        filename = os.path.join('champsim', 'results', 'task2a', f'{p}_{t}.txt')
        with open(filename, 'r') as f:
            content = f.read()
        
        # IPC: find last occurrence
        ipc_matches = re.findall(r'CPU 0 cumulative IPC:\s+([\d\.]+)', content)
        ipc = float(ipc_matches[-1]) if ipc_matches else None
        
        # L2C Total LOAD MPKI
        l2c_load_mpki_match = re.search(r'L2C LOAD\s+ACCESS:\s+\d+\s+HIT:\s+\d+\s+MISS:\s+\d+\s+HIT %:\s+[\d\.]+\s+MISS %:\s+[\d\.]+\s+MPKI:\s+([\d\.]+)', content)
        l2c_load_mpki = float(l2c_load_mpki_match.group(1)) if l2c_load_mpki_match else None
        
        # L2C DATA LOAD MPKI
        data_mpki_match = re.search(r'L2C DATA LOAD MPKI:\s+([\d\.]+)', content)
        data_mpki = float(data_mpki_match.group(1)) if data_mpki_match else None
        
        # L2C INSTRUCTION LOAD MPKI
        instr_mpki_match = re.search(r'L2C INSTRUCTION LOAD MPKI:\s+([\d\.]+)', content)
        instr_mpki = float(instr_mpki_match.group(1)) if instr_mpki_match else None
        
        results[p][t] = {
            'ipc': ipc,
            'l2c_load_mpki': l2c_load_mpki,
            'data_mpki': data_mpki,
            'instr_mpki': instr_mpki
        }

print("\n" + "="*80)
print(f"{'Trace':<8} | {'Policy':<10} | {'IPC':<8} | {'Speedup':<8} | {'L2C Load MPKI':<14} | {'L2 Instr MPKI':<14} | {'L2 Data MPKI':<14}")
print("="*80)

for t in traces:
    base_ipc = results['baseline'][t]['ipc']
    for p in policies:
        d = results[p][t]
        speedup = d['ipc'] / base_ipc if base_ipc else 1.0
        print(f"{t:<8} | {p.upper():<10} | {d['ipc']:<8.4f} | {speedup:<8.4f} | {d['l2c_load_mpki']:<14.4f} | {d['instr_mpki']:<14.4f} | {d['data_mpki']:<14.4f}")
    print("-" * 80)
