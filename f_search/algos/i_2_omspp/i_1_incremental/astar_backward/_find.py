from f_search.algos.i_2_omspp.i_1_incremental.astar_backward import (
    AStarIncrementalBackward)
from f_search.problems.i_2_omspp import ProblemOMSPP
import csv


def _run_incremental(problem: ProblemOMSPP,
                     depth: int,
                     is_analytics: bool = False
                     ) -> tuple[int, AStarIncrementalBackward] | None:
    """
    ========================================================================
     Run AStarIncrementalBackward and return (explored, algo).
    ========================================================================
    """
    algo = AStarIncrementalBackward(problem=problem,
                                    depth_propagation=depth,
                                    is_analytics=is_analytics)
    sol = algo.run()
    if not sol:
        return None
    return sol.stats.explored, algo


def _csv_explored(algo: AStarIncrementalBackward,
                  path: str) -> None:
    """
    ========================================================================
     Write explored States to a CSV file.
    ========================================================================
    """
    rows = algo.list_explored()
    if not rows:
        return
    fieldnames = ['depth'] + list(rows[0].keys())
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        depth = algo._depth_propagation
        for row in rows:
            writer.writerow({'depth': depth, **row})


def find(rows: int,
         pct_obstacles: int,
         n_goals: int,
         depth: int,
         tries: int) -> ProblemOMSPP | None:
    """
    ========================================================================
     Find a ProblemOMSPP where AStarIncrementalBackward(depth=-1) explores
      fewer states than repeated backward A* (no sharing).
    ========================================================================
    """
    for _ in range(tries):
        problem = ProblemOMSPP.Factory.custom(rows=rows,
                                              pct_obstacles=pct_obstacles,
                                              k=n_goals)
        result_a = _run_incremental(problem=problem,
                                    depth=depth,
                                    is_analytics=True)
        if not result_a:
            continue
        result_b = _run_incremental(problem=problem,
                                    depth=depth + 1,
                                    is_analytics=True)
        if not result_b:
            continue
        explored_a, algo_a = result_a
        explored_b, algo_b = result_b
        if explored_b < explored_a:
            _csv_explored(algo_a, path=csv_explored_a)
            _csv_explored(algo_b, path=csv_explored_b)
            return problem
    return None


folder_temp = 'f:\\temp\\2026\\03'
csv_explored_a = f'{folder_temp}\\explored_a.csv'
csv_explored_b = f'{folder_temp}\\explored_b.csv'
problem = find(rows=5, pct_obstacles=50, n_goals=2, depth=-1, tries=1_000)
if not problem:
    exit()
print(problem.grid.print())
print(problem.start)
print(problem.goals)
