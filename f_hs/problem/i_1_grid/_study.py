"""
============================================================================
 ProblemGrid — light pickling + parallel runner study.

 Sections:
   1. Raw pickle roundtrip on a single Problem (auto-detaches on load).
   2. Store.save / Store.load — N problems on shared Grids, split files,
      shared StateCell cache on load.
   3. Detached semantics — stable key/hash, .grid raises.
   4. Runner.run — parallel experiment over a saved batch.

 Module-level functions and __main__ guard are required so worker
 processes can import the module without re-running the demo.
============================================================================
"""
import os
import pickle
import tempfile
import time

from f_hs.problem.i_1_grid import ProblemGrid
from f_ds.grids.grid.map import GridMap


# ─── Module-level experiment (picklable, used by Runner workers) ────────

def experiment_stats(problem: ProblemGrid) -> dict:
    """
    ============================================================================
     Tiny experiment — return per-Problem stats plus a synthetic
     100 ms work burst so parallelism is visible in wall-clock time.
    ============================================================================
    """
    # Simulated search work
    time.sleep(0.1)
    return {
        'name': problem.name,
        'grid_name': problem.grid_name,
        'start_rc': problem.start_rc,
        'goal_rc': problem.goal_rc,
        'num_successors_start': len(problem.successors(problem.start)),
        'worker_pid': os.getpid(),
    }


# ─── Demos ─────────────────────────────────────────────────────────────

def demo_single_pickle_roundtrip() -> None:
    """
    ============================================================================
     1. Pickle one Problem → light. Load → detached. attach() → live.
    ============================================================================
    """
    print('=' * 72)
    print(' 1. Single-problem raw pickle roundtrip')
    print('=' * 72)

    grid = GridMap(rows=30, cols=30, name='city')
    problem = ProblemGrid(grid=grid,
                          start=grid[0][0],
                          goal=grid[29][29],
                          name='p1')

    heavy_bytes = pickle.dumps(problem.__dict__)
    light_bytes = pickle.dumps(problem)
    print(f'heavy (full __dict__):  {len(heavy_bytes):>7} bytes')
    print(f'light (ProblemGrid):    {len(light_bytes):>7} bytes')
    print(f'reduction:              '
          f'{len(light_bytes) / len(heavy_bytes):.1%}')

    loaded: ProblemGrid = pickle.loads(light_bytes)
    print(f'\nafter pickle.loads:     is_attached={loaded.is_attached}')
    print(f'stable identity:        grid_name={loaded.grid_name!r}, '
          f'start_rc={loaded.start_rc}, goal_rc={loaded.goal_rc}')

    loaded.attach(grid=grid)
    children = loaded.successors(loaded.start)
    print(f'after attach(grid):     is_attached={loaded.is_attached}, '
          f'successors({loaded.start.rc})='
          f'{sorted(s.rc for s in children)}')


def demo_store_roundtrip() -> None:
    """
    ============================================================================
     2. Store.save / Store.load — multi-problem, split-file persistence.
    ============================================================================
    """
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
        print(f'naive (problems × full __dict__):  '
              f'{naive_bytes:>7} bytes')
        print(f'split problems.pkl:                {size_p:>7} bytes')
        print(f'split grids.pkl:                   {size_g:>7} bytes')
        print(f'split total:                       '
              f'{split_bytes:>7} bytes  '
              f'({split_bytes / naive_bytes:.1%})')

        loaded_problems, _ = ProblemGrid.Store.load(
            path_problems=path_p,
            path_grids=path_g)

    arena_problems = [p for p in loaded_problems
                      if p.grid_name == 'arena']
    ids = {id(p._states) for p in arena_problems}
    print(f'\narena problems:                   {len(arena_problems)}')
    print(f'distinct _states dict objects:    {len(ids)}   '
          f'(→ 1 = fully shared)')


def demo_detached_semantics() -> None:
    """
    ============================================================================
     3. Detached semantics — stable key/hash; .grid access raises.
    ============================================================================
    """
    print('\n' + '=' * 72)
    print(' 3. Detached semantics')
    print('=' * 72)

    grid = GridMap(rows=10, cols=10, name='d')
    p = ProblemGrid(grid=grid,
                    start=grid[0][0],
                    goal=grid[9][9],
                    name='demo')
    k_before, h_before = p.key, hash(p)
    p.detach()
    print(f'key stable across detach:  {p.key == k_before}')
    print(f'hash stable across detach: {hash(p) == h_before}')
    try:
        _ = p.grid
    except RuntimeError as e:
        print(f'detached .grid raised:     RuntimeError: {e}')


def demo_parallel_runner() -> None:
    """
    ============================================================================
     4. Runner.run — spawn a ProcessPoolExecutor over a saved batch.
        Grids load once per worker; detached problems are shipped as
        light pickles per task; experiment_stats sleeps 100 ms to make
        parallelism visible in wall-clock time.
    ============================================================================
    """
    print('\n' + '=' * 72)
    print(' 4. Runner.run — parallel experiment over saved batch')
    print('=' * 72)

    grid = GridMap(rows=40, cols=40, name='arena')
    problems = [
        ProblemGrid(grid=grid,
                    start=grid[0][0],
                    goal=grid[r][c],
                    name=f'p_{r:02d}_{c:02d}')
        for r, c in [(10, 10), (10, 30), (20, 20),
                     (30, 10), (30, 30), (39, 39),
                     (5, 35), (35, 5)]
    ]

    with tempfile.TemporaryDirectory() as d:
        path_p = os.path.join(d, 'problems.pkl')
        path_g = os.path.join(d, 'grids.pkl')
        ProblemGrid.Store.save(problems=problems,
                               grids={'arena': grid},
                               path_problems=path_p,
                               path_grids=path_g)

        for workers in (1, 4):
            t0 = time.perf_counter()
            results = ProblemGrid.Runner.run(
                path_problems=path_p,
                path_grids=path_g,
                experiment=experiment_stats,
                workers=workers,
                chunksize=1)
            elapsed = time.perf_counter() - t0
            pids = {r['worker_pid'] for r in results}
            print(f'workers={workers}:  '
                  f'{len(results)} results in {elapsed:.2f}s  '
                  f'across {len(pids)} worker PIDs')

    # Show a sample result
    sample = results[0]
    print(f'\nsample result: {sample}')


if __name__ == '__main__':
    demo_single_pickle_roundtrip()
    demo_store_roundtrip()
    demo_detached_semantics()
    demo_parallel_runner()
