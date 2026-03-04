import csv
from f_search.algos.i_1_spp import AStarCached

astar = AStarCached.Factory.with_cache()
astar.run()
rows = astar.list_explored()

path = 'f:\\temp\\2026\\03\\with_cache.csv'
with open(path, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
print(f'Saved {len(rows)} rows to {path}')
