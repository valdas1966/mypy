"""
============================================================================
 ProblemGrid — light pickling study.

 Shows:
   1. Pickle a Problem → grid and StateCell cache are dropped.
   2. Load the Problem → it is DETACHED; successors() would raise.
   3. attach(grid) → Problem is live again.
   4. Store.save/load → many Problems on few Grids, files split.
============================================================================
"""
import os
import pickle
import tempfile

from f_hs.problem.i_1_grid import ProblemGrid
from f_ds.grids.grid.map import GridMap


# ─── 1. Single-problem roundtrip via raw pickle ──────────────────────────

print('=' * 72)
print(' 1. Single-problem raw pickle roundtrip')
print('=' * 72)

grid = GridMap(rows=30, cols=30, name='city')
problem = ProblemGrid(grid=grid,
                      start=grid[0][0],
                      goal=grid[29][29],
                      name='p1')

# Size: what the __dict__ would weigh if we pickled it whole.
heavy_bytes = pickle.dumps(problem.__dict__)
# Size: what the problem actually pickles to (light — drops grid+states).
light_bytes = pickle.dumps(problem)

print(f'heavy (full __dict__):  {len(heavy_bytes):>7} bytes')
print(f'light (ProblemGrid):    {len(light_bytes):>7} bytes')
print(f'reduction:              {len(light_bytes) / len(heavy_bytes):.1%}')

# Round-trip
loaded: ProblemGrid = pickle.loads(light_bytes)
print(f'\nafter pickle.loads:     is_attached={loaded.is_attached}')
print(f'stable identity:        grid_name={loaded.grid_name!r}, '
      f'start_rc={loaded.start_rc}, goal_rc={loaded.goal_rc}')

# Rehydrate manually
loaded.attach(grid=grid)
children = loaded.successors(loaded.start)
print(f'after attach(grid):     is_attached={loaded.is_attached}, '
      f'successors({loaded.start.rc})='
      f'{sorted(s.rc for s in children)}')


# ─── 2. Store: N problems on 2 grids, two-file save/load ─────────────────

print('\n' + '=' * 72)
print(' 2. Store.save / Store.load — 5 problems on 2 shared grids')
print('=' * 72)

grid_a = GridMap(rows=50, cols=50, name='arena')
grid_b = GridMap(rows=50, cols=50, name='tel_aviv')

problems = [
    ProblemGrid(grid=grid_a, start=grid_a[0][0],
                goal=grid_a[49][49], name='a_corner'),
    ProblemGrid(grid=grid_a, start=grid_a[0][0],
                goal=grid_a[25][25], name='a_center'),
    ProblemGrid(grid=grid_a, start=grid_a[10][10],
                goal=grid_a[40][40], name='a_mid'),
    ProblemGrid(grid=grid_b, start=grid_b[0][0],
                goal=grid_b[49][49], name='b_corner'),
    ProblemGrid(grid=grid_b, start=grid_b[5][5],
                goal=grid_b[45][45], name='b_inner'),
]
grids = {'arena': grid_a, 'tel_aviv': grid_b}

# Baseline: naively pickling each Problem's full __dict__ (simulating
# what we would pay WITHOUT the detach + split-file design).
naive_bytes = sum(len(pickle.dumps(p.__dict__)) for p in problems)

with tempfile.TemporaryDirectory() as d:
    path_p = os.path.join(d, 'problems.pkl')
    path_g = os.path.join(d, 'grids.pkl')
    ProblemGrid.Store.save(problems=problems,
                           grids=grids,
                           path_problems=path_p,
                           path_grids=path_g)
    size_p = os.path.getsize(path_p)
    size_g = os.path.getsize(path_g)
    split_bytes = size_p + size_g
    print(f'naive (problems × full __dict__):  {naive_bytes:>7} bytes')
    print(f'split problems.pkl:                {size_p:>7} bytes')
    print(f'split grids.pkl:                   {size_g:>7} bytes')
    print(f'split total:                       {split_bytes:>7} bytes')
    print(f'reduction:                         '
          f'{split_bytes / naive_bytes:.1%}')

    loaded_problems, loaded_grids = ProblemGrid.Store.load(
        path_problems=path_p,
        path_grids=path_g)

# Shared StateCell cache across problems on the same grid.
arena_problems = [p for p in loaded_problems if p.grid_name == 'arena']
ids = {id(p._states) for p in arena_problems}
print(f'\narena problems:                   {len(arena_problems)}')
print(f'distinct _states dict objects:    {len(ids)}   '
      f'(→ 1 = fully shared)')

# All problems are usable — verify one.
p = loaded_problems[0]
print(f'\nsample roundtrip — {p.name!r} ({p.grid_name}):')
print(f'  is_attached = {p.is_attached}')
print(f'  start.rc    = {p.start.rc}')
print(f'  successors  = {sorted(s.rc for s in p.successors(p.start))}')


# ─── 3. Detached semantics ───────────────────────────────────────────────

print('\n' + '=' * 72)
print(' 3. Detached semantics — key/hash are stable; grid access raises')
print('=' * 72)

p = ProblemGrid(grid=grid_a, start=grid_a[0][0],
                goal=grid_a[9][9], name='demo')
k_before, h_before = p.key, hash(p)
p.detach()
print(f'before / after detach — key equal:  {p.key == k_before}')
print(f'before / after detach — hash equal: {hash(p) == h_before}')
try:
    _ = p.grid
except RuntimeError as e:
    print(f'detached .grid raised RuntimeError: {e}')
