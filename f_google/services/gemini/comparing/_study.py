"""
============================================================================
 Benchmark: ask() vs ask_str() runtime comparison.
 Runs 1000 calls per method, saves per-call elapsed times to CSV.
 Analysis uses subsets at n ∈ [1, 10, 100, 1000].
============================================================================
"""
import csv
import time
from f_google.services.gemini import Gemini

PROMPT = 'Reply with only the number: 2+2='
N_MAX = 100
CSV_PATH = 'benchmark.csv'

gemini = Gemini.Factory.rami()

rows = []
for method_name in ['ask', 'ask_str']:
    print(f'\n--- {method_name} ({N_MAX} calls) ---')
    for i in range(N_MAX):
        t0 = time.perf_counter()
        if method_name == 'ask':
            gemini.ask(prompt=PROMPT)
        else:
            gemini.ask_str(prompt=PROMPT)
        elapsed = time.perf_counter() - t0
        rows.append({'method': method_name,
                     'index': i,
                     'elapsed': elapsed})
        if (i + 1) % 10 == 0:
            print(f'  {i + 1}/{N_MAX} done')

# Save to CSV
with open(CSV_PATH, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['method', 'index', 'elapsed'])
    writer.writeheader()
    writer.writerows(rows)

print(f'\nSaved {len(rows)} rows to {CSV_PATH}')
