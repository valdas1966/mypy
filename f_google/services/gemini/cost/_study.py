"""
============================================================================
 Cost Study: run ask() 100 times and log Response repr to CSV.
============================================================================
"""
import csv
from f_google.services.gemini import Gemini

PROMPT = 'Reply with only the number: 2+2='
N = 100
CSV_PATH = 'benchmark_cost.csv'

gemini = Gemini.Factory.rami()

rows = []
for i in range(N):
    response = gemini.ask(prompt=PROMPT)
    rows.append({'index': i, 'repr': repr(response)})
    if (i + 1) % 10 == 0:
        print(f'  {i + 1}/{N} done  |  {repr(response)}')

with open(CSV_PATH, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['index', 'repr'])
    writer.writeheader()
    writer.writerows(rows)

print(f'\nSaved {len(rows)} rows to {CSV_PATH}')
