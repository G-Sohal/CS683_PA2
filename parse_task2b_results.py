import re
import os

traces = ['Trace1', 'Trace2', 'Trace3']
thresholds = ['th15', 'th20', 'th25', 'th30', 'th35']
th_values = {'th15': 0.15, 'th20': 0.20, 'th25': 0.25, 'th30': 0.30, 'th35': 0.35}

# Load baseline and irrip values from task2a
baseline_ipc = {}
for t in traces:
    fn = os.path.join('champsim', 'results', 'task2a', f'baseline_{t}.txt')
    with open(fn, 'r') as f:
        matches = re.findall(r'CPU 0 cumulative IPC:\s+([\d\.]+)', f.read())
        baseline_ipc[t] = float(matches[-1])

results_2b = {}

for th in thresholds:
    results_2b[th] = {}
    for t in traces:
        filename = os.path.join('champsim', 'results', 'task2b', f'dyn_irrip_{th}_{t}.txt')
        with open(filename, 'r') as f:
            content = f.read()
        
        ipc_matches = re.findall(r'CPU 0 cumulative IPC:\s+([\d\.]+)', content)
        ipc = float(ipc_matches[-1]) if ipc_matches else None
        
        l2c_load_mpki_match = re.search(r'L2C LOAD\s+ACCESS:\s+\d+\s+HIT:\s+\d+\s+MISS:\s+\d+\s+HIT %:\s+[\d\.]+\s+MISS %:\s+[\d\.]+\s+MPKI:\s+([\d\.]+)', content)
        l2c_load_mpki = float(l2c_load_mpki_match.group(1)) if l2c_load_mpki_match else None
        
        data_mpki_match = re.search(r'L2C DATA LOAD MPKI:\s+([\d\.]+)', content)
        data_mpki = float(data_mpki_match.group(1)) if data_mpki_match else None
        
        instr_mpki_match = re.search(r'L2C INSTRUCTION LOAD MPKI:\s+([\d\.]+)', content)
        instr_mpki = float(instr_mpki_match.group(1)) if instr_mpki_match else None
        
        results_2b[th][t] = {
            'ipc': ipc,
            'speedup': ipc / baseline_ipc[t],
            'l2c_load_mpki': l2c_load_mpki,
            'data_mpki': data_mpki,
            'instr_mpki': instr_mpki
        }

print("\n" + "="*85)
print(f"{'Trace':<8} | {'Threshold':<10} | {'IPC':<8} | {'Speedup':<8} | {'L2C Load MPKI':<14} | {'L2 Instr MPKI':<14} | {'L2 Data MPKI':<14}")
print("="*85)

for t in traces:
    for th in thresholds:
        d = results_2b[th][t]
        val = th_values[th]
        print(f"{t:<8} | {val:<10.2f} | {d['ipc']:<8.4f} | {d['speedup']:<8.4f} | {d['l2c_load_mpki']:<14.4f} | {d['instr_mpki']:<14.4f} | {d['data_mpki']:<14.4f}")
    print("-" * 85)
