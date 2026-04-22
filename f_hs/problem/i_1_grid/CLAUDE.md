# ProblemGrid

## Purpose
Shortest-Path-Problem on a 2D GridMap. Successors are valid
grid neighbors. Caches StateCell objects for efficiency.

Supports **light pickling** — the heavy grid and StateCell cache
are dropped on `__getstate__` and rehydrated via `attach(grid)`.
Bulk save/load of many problems sharing a few grids is handled by
the `Store` helper (problems -> one pickle, grids -> another).

## Public API

### Constructor
```python
def __init__(self, grid: GridMap, start: CellMap,
             goal: CellMap, name: str = 'ProblemGrid') -> None
```

### Properties
| Property | Type | Description |
|----------|------|-------------|
| `grid` | `GridMap` | The attached grid (raises if detached) |
| `grid_name` | `str` | Stable grid identifier (survives pickle) |
| `start_rc` | `tuple[int, int]` | Start coords (stable) |
| `goal_rc` | `tuple[int, int]` | Goal coords (stable) |
| `is_attached` | `bool` | True when grid is attached |
| `key` | `tuple` | `(grid_name, start_rc, goal_rc)` — stable |

### Methods
| Method | Description |
|--------|-------------|
| `successors(state)` | Valid grid neighbors |
| `attach(grid, states=None)` | Rehydrate with a grid; optional shared `dict[CellMap, StateCell]` cache |
| `detach()` | Drop grid and state cache (for light persistence) |

### Pickle Behavior
- `__getstate__` — drops `_grid`, `_states`, `_starts`, `_goals`.
- `__setstate__` — restores light state; problem is **detached** until `attach()` is called.
- `key` and `__hash__` are based on `(grid_name, start_rc, goal_rc)` and remain stable across detach / pickle.

## Factory
| Method | Description |
|--------|-------------|
| `grid_3x3()` | Open 3x3, (0,0)->(2,2), cost 4 |
| `grid_3x3_obstacle()` | Obstacle at (1,1), cost 4 |
| `grid_3x3_no_path()` | Wall across middle row |
| `grid_3x3_start_is_goal()` | Start == Goal |
| `grid_4x4_obstacle()` | 2-cell wall at (0,2),(1,2); (0,0)->(0,3), cost 7 |

## Store (bulk save / load)

`ProblemGrid.Store` persists many problems plus their grids across
two separate pickle files. On load, Problems sharing a grid share
**one** `StateCell` cache — so N problems on a single 1M-cell grid
allocate 1M StateCell objects total, not N × 1M.

| Method | Description |
|--------|-------------|
| `save(problems, grids, path_problems, path_grids)` | Pickle detached problems + grids dict |
| `load(path_problems, path_grids, bind=True)` | Load both files; bind by default |
| `bind(problems, grids)` | Attach problems to grids with shared per-grid state cache |

### Save / Load Example
```python
from f_hs.problem.i_1_grid import ProblemGrid

# Save
ProblemGrid.Store.save(
    problems=[p1, p2, p3],
    grids={'arena': g_arena, 'tel_aviv': g_tel_aviv},
    path_problems='/tmp/problems.pkl',
    path_grids='/tmp/grids.pkl',
)

# Load (auto-bind, shared StateCell cache per grid)
problems, grids = ProblemGrid.Store.load(
    path_problems='/tmp/problems.pkl',
    path_grids='/tmp/grids.pkl',
)
```

### Validation at save-time
- Every `problem.grid_name` must appear in the `grids` dict.
- Each grid's `name` attribute must equal its dict key.

## Design Decisions

- **Grid identity via `GridMap.name`.** Strings are human-readable and picklable; the `Store` validates uniqueness at save time.
- **Stable key / hash.** `key = (grid_name, start_rc, goal_rc)` so problems can live in sets / dicts even when detached.
- **Shared StateCell cache per grid.** `Store.bind()` allocates one `dict[CellMap, StateCell]` per distinct grid and hands the same reference to every problem on that grid. Cuts memory O(N × cells) → O(cells) when N problems share a grid.
- **Manual `attach(grid, states=)` stays public.** Lets callers wire up shared caches without going through `Store` when building problem sets programmatically.

## Runner (parallel experiment execution)

`ProblemGrid.Runner` spawns a `ProcessPoolExecutor` over a saved
batch and runs an arbitrary picklable `experiment` callable on
each Problem. Grids are loaded **once per worker** at init time;
per-task IPC payload is only the light detached Problem plus the
experiment return value. Each worker also pre-builds **one shared
StateCell cache per grid**, so all tasks on that worker share the
same dict (same optimization as `Store.bind`, repeated per-process).

| Method | Description |
|--------|-------------|
| `run(path_problems, path_grids, experiment, workers=None, chunksize=1)` | Run experiment over all problems; returns list of results in submission order |

### Contract
- `experiment` must be picklable — **module-level functions** or
  picklable callable classes. Lambdas / closures won't ship across
  process boundaries.
- `workers=None` → `os.cpu_count()`.
- `chunksize=1` is right for long tasks (seconds). For short tasks
  (ms), raise to 32-100 to amortize IPC overhead.

### Example
```python
# at module level — required for pickling into workers
def experiment(problem: ProblemGrid) -> dict:
    algo = AStar(problem=problem)
    sol = algo.run()
    return {'name': problem.name, 'cost': sol.cost,
            'elapsed': algo.elapsed}

results = ProblemGrid.Runner.run(
    path_problems='/tmp/problems.pkl',
    path_grids='/tmp/grids.pkl',
    experiment=experiment,
    workers=8,
    chunksize=16,
)
```

### Memory Tradeoff
Grid is held in each worker's memory → total grid footprint is
`size(grid) × workers`. For 1 GB grids × 8 workers = 8 GB. If this
bites, shared-memory redesign is the next step (not implemented).

## Study Script

`_study.py` — runnable walkthrough of the full design.
Run with `python -m f_hs.problem.i_1_grid._study`. Shows:
1. Raw `pickle.dumps/loads` on a single Problem (detached on load).
2. `Store.save/load` on N Problems over 2 Grids — compares naive vs
   split-file sizes and shows the shared StateCell cache on load.
3. Detached semantics — stable `key`/`hash`, `.grid` access raises.
4. `Runner.run` — parallel experiment over a saved batch; prints
   wall-clock time for `workers=1` vs `workers=4`.

## Dependencies
- `f_hs.problem.i_0_base.ProblemSPP`
- `f_hs.state.i_1_cell.StateCell`
- `f_ds.grids.cell.i_1_map.CellMap`
- `f_ds.grids.grid.map.GridMap`
