import pickle
from concurrent.futures import ProcessPoolExecutor
from typing import Any, Callable, TypeVar

from f_hs.problem.i_1_grid.main import ProblemGrid
from f_hs.state.i_1_cell.main import StateCell
from f_ds.grids.grid.map import GridMap

R = TypeVar('R')

# ─── Process-global state (set by _worker_init per worker) ──────────────
_WORKER_GRIDS: dict[str, GridMap] | None = None
_WORKER_CACHES: dict[str, dict] | None = None
_WORKER_EXP: Callable[[ProblemGrid], Any] | None = None


def _worker_init(path_grids: str,
                 experiment: Callable[[ProblemGrid], Any]) -> None:
    """
    ============================================================================
     Worker initializer — runs once per worker process.

     Loads the grids pickle into process-global memory, builds a shared
     StateCell cache per grid, and stores the experiment callable. All
     subsequent tasks on this worker reuse these without re-loading.
    ============================================================================
    """
    global _WORKER_GRIDS, _WORKER_CACHES, _WORKER_EXP
    with open(path_grids, 'rb') as f:
        _WORKER_GRIDS = pickle.load(f)
    _WORKER_CACHES = {name: {c: StateCell(key=c) for c in grid}
                      for name, grid in _WORKER_GRIDS.items()}
    _WORKER_EXP = experiment


def _worker_task(problem: ProblemGrid) -> Any:
    """
    ============================================================================
     Worker task — attaches the detached Problem to its Grid and runs the
     experiment. Returns whatever the experiment returns (must be picklable).
    ============================================================================
    """
    problem.attach(grid=_WORKER_GRIDS[problem.grid_name],
                   states=_WORKER_CACHES[problem.grid_name])
    return _WORKER_EXP(problem)


class Runner:
    """
    ============================================================================
     Parallel experiment runner for ProblemGrid batches.

     Loads detached problems from disk, ships them to a pool of worker
     processes, and each worker loads the grids pickle exactly once at
     init time (with a shared StateCell cache per grid). Per-task IPC
     payload is only the light detached Problem plus the experiment
     return value — the heavy grids stay in worker memory.
    ============================================================================
    """

    @staticmethod
    def run(path_problems: str,
            path_grids: str,
            experiment: Callable[[ProblemGrid], R],
            workers: int | None = None,
            chunksize: int = 1) -> list[R]:
        """
        ========================================================================
         Run the experiment over every Problem in `path_problems`.

         Parameters
           - `path_problems`: detached-problem pickle produced by Store.save.
           - `path_grids`: grids pickle produced by Store.save.
           - `experiment`: picklable callable invoked on each attached
             Problem; its return value is accumulated into the result list.
           - `workers`: number of worker processes (None → os.cpu_count()).
           - `chunksize`: tasks per IPC round-trip — raise for short tasks.

         Returns a list of experiment return values in Problem order.
        ========================================================================
        """
        with open(path_problems, 'rb') as f:
            problems: list[ProblemGrid] = pickle.load(f)
        with ProcessPoolExecutor(
                max_workers=workers,
                initializer=_worker_init,
                initargs=(path_grids, experiment)) as pool:
            return list(pool.map(_worker_task,
                                 problems,
                                 chunksize=chunksize))
