import os
import tempfile

from f_hs.problem.i_1_grid import ProblemGrid
from f_ds.grids.grid.map import GridMap


def _exp_stats(problem: ProblemGrid) -> dict:
    """
    ============================================================================
     Picklable experiment — compute basic per-Problem stats. Must be at
     module level so ProcessPoolExecutor workers can unpickle it.
    ============================================================================
    """
    return {
        'name': problem.name,
        'grid_name': problem.grid_name,
        'start_rc': problem.start_rc,
        'goal_rc': problem.goal_rc,
        'num_start_successors': len(problem.successors(problem.start)),
        'num_grid_cells': len(problem.grid),
    }


def _exp_pid(problem: ProblemGrid) -> int:
    """
    ============================================================================
     Experiment returning the worker process PID — used to verify that
     tasks actually fan out across multiple workers.
    ============================================================================
    """
    return os.getpid()


def _save(problems, grids, d):
    """
    ============================================================================
     Save Problems + Grids under a temp dir; return the two file paths.
    ============================================================================
    """
    path_p = os.path.join(d, 'problems.pkl')
    path_g = os.path.join(d, 'grids.pkl')
    ProblemGrid.Store.save(problems=problems,
                           grids=grids,
                           path_problems=path_p,
                           path_grids=path_g)
    return path_p, path_g


def test_runner_single_worker_matches_direct_call() -> None:
    """
    ========================================================================
     With a single worker, Runner results must match a direct in-process
     call of the experiment on each Problem.
    ========================================================================
    """
    grid = GridMap(rows=5, cols=5, name='g')
    problems = [
        ProblemGrid(grid=grid, start=grid[0][0],
                    goal=grid[4][4], name='p1'),
        ProblemGrid(grid=grid, start=grid[0][0],
                    goal=grid[2][2], name='p2'),
        ProblemGrid(grid=grid, start=grid[1][1],
                    goal=grid[3][3], name='p3'),
    ]
    expected = [_exp_stats(p) for p in problems]
    with tempfile.TemporaryDirectory() as d:
        pp, pg = _save(problems, {'g': grid}, d)
        got = ProblemGrid.Runner.run(path_problems=pp,
                                     path_grids=pg,
                                     experiment=_exp_stats,
                                     workers=1)
    assert got == expected


def test_runner_preserves_order() -> None:
    """
    ========================================================================
     Runner.run returns results in Problem-submission order even with
     multiple workers executing out of order.
    ========================================================================
    """
    grid = GridMap(rows=4, cols=4, name='g')
    problems = [
        ProblemGrid(grid=grid, start=grid[0][0],
                    goal=grid[3][3], name=f'p{i}')
        for i in range(6)
    ]
    with tempfile.TemporaryDirectory() as d:
        pp, pg = _save(problems, {'g': grid}, d)
        got = ProblemGrid.Runner.run(path_problems=pp,
                                     path_grids=pg,
                                     experiment=_exp_stats,
                                     workers=2)
    assert [r['name'] for r in got] == [p.name for p in problems]


def test_runner_multi_grid_each_problem_sees_own_grid() -> None:
    """
    ========================================================================
     Problems on different grids are each attached to the correct grid
     inside the workers (grid_name → grid lookup works).
    ========================================================================
    """
    ga = GridMap(rows=3, cols=3, name='small')
    gb = GridMap(rows=6, cols=6, name='big')
    problems = [
        ProblemGrid(grid=ga, start=ga[0][0], goal=ga[2][2], name='sa'),
        ProblemGrid(grid=gb, start=gb[0][0], goal=gb[5][5], name='ba'),
        ProblemGrid(grid=ga, start=ga[1][1], goal=ga[2][2], name='sb'),
        ProblemGrid(grid=gb, start=gb[2][2], goal=gb[5][5], name='bb'),
    ]
    with tempfile.TemporaryDirectory() as d:
        pp, pg = _save(problems, {'small': ga, 'big': gb}, d)
        got = ProblemGrid.Runner.run(path_problems=pp,
                                     path_grids=pg,
                                     experiment=_exp_stats,
                                     workers=2)
    by_name = {r['name']: r for r in got}
    assert by_name['sa']['num_grid_cells'] == 9
    assert by_name['ba']['num_grid_cells'] == 36
    assert by_name['sb']['num_grid_cells'] == 9
    assert by_name['bb']['num_grid_cells'] == 36


def test_runner_fans_out_across_workers() -> None:
    """
    ========================================================================
     With >1 worker and enough tasks, results span >1 distinct PID —
     confirms true process-level parallelism.
    ========================================================================
    """
    grid = GridMap(rows=3, cols=3, name='g')
    problems = [
        ProblemGrid(grid=grid, start=grid[0][0],
                    goal=grid[2][2], name=f'p{i}')
        for i in range(16)
    ]
    with tempfile.TemporaryDirectory() as d:
        pp, pg = _save(problems, {'g': grid}, d)
        pids = ProblemGrid.Runner.run(path_problems=pp,
                                      path_grids=pg,
                                      experiment=_exp_pid,
                                      workers=2,
                                      chunksize=1)
    assert len(set(pids)) >= 2
    assert os.getpid() not in set(pids)
