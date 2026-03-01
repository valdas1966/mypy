from f_search.algos.i_2_omspp.i_1_incremental.astar_backward import (
    AStarIncrementalBackward)
from f_search.algos.i_1_spp import AStar
from f_search.problems.i_2_omspp import ProblemOMSPP


def _explored_repeated(problem: ProblemOMSPP) -> int | None:
    """
    ========================================================================
     Return total explored states for repeated backward A* (no sharing).
    ========================================================================
    """
    total = 0
    for spp in problem.to_spps():
        algo = AStar(problem=spp.reverse())
        sol = algo.run()
        if not sol:
            return None
        total += sol.stats.explored
    return total


def _explored_incremental(problem: ProblemOMSPP,
                          depth: int) -> int | None:
    """
    ========================================================================
     Return total explored states for AStarIncrementalBackward.
    ========================================================================
    """
    algo = AStarIncrementalBackward(problem=problem,
                                    depth_propagation=depth)
    sol = algo.run()
    if not sol:
        return None
    return sol.stats.explored


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
        explored_a = _explored_incremental(problem=problem, depth=depth)
        if explored_a is None:
            continue
        explored_b = _explored_incremental(problem=problem, depth=depth+1)
        if explored_b < explored_a:
            return problem
    return None


problem = find(rows=5, pct_obstacles=50, n_goals=2, depth=-1, tries=1_000)
if not problem:
    exit()
print(problem.grid.print())
print(problem.start)
print(problem.goals)