from f_search.algos.i_2_omspp.i_1_incremental.astar_backward import (
    AStarIncrementalBackward)
from f_search.problems.i_2_omspp import ProblemOMSPP


def _explored_at_depth(problem: ProblemOMSPP,
                       depth: int) -> int | None:
    """
    ========================================================================
     Return total explored states for the second sub-search at given depth.
    ========================================================================
    """
    algo = AStarIncrementalBackward(problem=problem,
                                    depth_propagation=depth)
    solution = algo.run()
    if not solution:
        return None
    # Second sub-solution's explored count
    sub_solutions = algo._sub_solutions
    if len(sub_solutions) < 2:
        return None
    return sub_solutions[1].stats.explored


def is_exploiting_all_features(problem: ProblemOMSPP) -> bool:
    """
    ========================================================================
     Check if each incremental feature level reduces explored states.
    ========================================================================
     depth=-1: cached exact distances only.
     depth= 0: cached + lower bounds from explored states.
     depth= 2: cached + lower bounds + propagation (depth=2).
     Returns True only if: explored_-1 > explored_0 > explored_2
    ========================================================================
    """
    e_neg1 = _explored_at_depth(problem=problem, depth=-1)
    e_0 = _explored_at_depth(problem=problem, depth=0)
    e_2 = _explored_at_depth(problem=problem, depth=2)
    if None in (e_neg1, e_0, e_2):
        return False
    return e_neg1 > e_0 > e_2


def print_explored(problem: ProblemOMSPP) -> None:
    """
    ========================================================================
     Print explored counts at each feature level for debugging.
    ========================================================================
    """
    results = {}
    for depth in [-1, 0, 2]:
        e = _explored_at_depth(problem=problem, depth=depth)
        results[depth] = e
        print(f'  depth={depth:2d}: explored={e}')
    vals = list(results.values())
    if None not in vals and vals[0] > vals[1] > vals[2]:
        print('  => ALL LEVELS SHOW STRICT IMPROVEMENT')
    else:
        print('  => Not all levels improve')


def print_problem(problem: ProblemOMSPP) -> None:
    """
    ========================================================================
     Print the problem layout for factory recreation.
    ========================================================================
    """
    grid = problem.grid
    start = problem.start
    start_rc = (start.key.row, start.key.col)
    goals_map = {}
    for i, goal in enumerate(problem.goals):
        goals_map[(goal.key.row, goal.key.col)] = f'G{i}'
    print(f'Grid: {grid.rows}x{grid.cols}')
    print(f'Start: {start_rc}')
    for rc, label in sorted(goals_map.items()):
        print(f'{label}: {rc}')
    print()
    for row in range(grid.rows):
        cells = []
        for col in range(grid.cols):
            cell = grid[row][col]
            rc = (row, col)
            if rc == start_rc:
                cells.append(' S ')
            elif rc in goals_map:
                cells.append(f' {goals_map[rc]}')
            elif not cell:
                cells.append(' X ')
            else:
                cells.append(' . ')
        print(f'  {row} [{"".join(cells)}]')
    print('\nObstacles:')
    for row in range(grid.rows):
        for col in range(grid.cols):
            if not grid[row][col]:
                print(f'  grid[{row}][{col}].set_invalid()')


def find_problem(rows: int = 5,
                 pct_obstacles: int = 50,
                 max_attempts: int = 100_000) -> ProblemOMSPP | None:
    """
    ========================================================================
     Search for a ProblemOMSPP that exploits all features.
    ========================================================================
    """
    for i in range(max_attempts):
        problem = ProblemOMSPP.Factory.custom(rows=rows,
                                              pct_obstacles=pct_obstacles,
                                              k=2)
        if is_exploiting_all_features(problem=problem):
            print(f'Found after {i + 1} attempts '
                  f'(rows={rows}, pct={pct_obstacles}%)')
            return problem
    return None


# Search across grid sizes
for rows in [10, 20, 30]:
    problem = find_problem(rows=rows,
                           max_attempts=1_000)
    if problem:
        print_explored(problem=problem)
        print()
        print_problem(problem=problem)
        exit()
    print(f'  {rows}x{rows}: not found in 1K attempts')
print('No problem found.')
