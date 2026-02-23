from f_utils import u_pickle
from f_search.problems import ProblemOMSPP as Problem
from f_ds.grids import GridMap as Grid
from pathlib import Path
import csv


def load_problems(path_problems: str) -> list[Problem]:
    """
    ============================================================================
     Load problems from pickle file.
    ============================================================================
    """
    return u_pickle.load(path=path_problems)


def load_grids(path_grids: str) -> dict[str, Grid]:
    """
    ============================================================================
     Load grids from pickle file.
    ============================================================================
    """
    return u_pickle.load(path=path_grids)


def calc_avg_dist_start_to_goals(problem: Problem) -> float:
    """
    ============================================================================
     Calculate average distance from start to all goals.
    ============================================================================
    """
    start_cell = problem.start.key
    distances = [start_cell.distance(goal.key) for goal in problem.goals]
    return sum(distances) / len(distances)


def calc_avg_dist_between_goals(problem: Problem) -> float:
    """
    ============================================================================
     Calculate average distance between all pairs of goals.
    ============================================================================
    """
    goals = problem.goals
    k = len(goals)
    total_dist = 0
    num_pairs = 0
    for i in range(k):
        for j in range(i + 1, k):
            total_dist += goals[i].key.distance(goals[j].key)
            num_pairs += 1
    return total_dist / num_pairs if num_pairs > 0 else 0


def calc_max_manhattan_dist(rows: int, cols: int) -> int:
    """
    ============================================================================
     Calculate max possible Manhattan distance in a grid.
    ============================================================================
    """
    return (rows - 1) + (cols - 1)


def normalize_dist(dist: float, max_dist: int) -> float:
    """
    ============================================================================
     Normalize distance to 0-100%.
    ============================================================================
    """
    return (dist / max_dist) * 100 if max_dist > 0 else 0


def calc_relative_position(value: int, max_value: int) -> float:
    """
    ============================================================================
     Normalize position to 0-99% (as if grid was 100x100).
    ============================================================================
    """
    return (value / max_value) * 99 if max_value > 0 else 0


def calc_avg_goal_position(problem: Problem) -> tuple[float, float]:
    """
    ============================================================================
     Calculate average row and col of all goals.
    ============================================================================
    """
    goals = problem.goals
    avg_row = sum(goal.key.row for goal in goals) / len(goals)
    avg_col = sum(goal.key.col for goal in goals) / len(goals)
    return avg_row, avg_col


def problem_to_row(problem: Problem, grid: Grid) -> dict:
    """
    ============================================================================
     Convert a problem to a CSV row dictionary.
    ============================================================================
    """
    rows, cols = grid.rows, grid.cols
    max_dist = calc_max_manhattan_dist(rows, cols)

    # Distances
    dist_start_goals = calc_avg_dist_start_to_goals(problem)
    dist_between_goals = calc_avg_dist_between_goals(problem)

    # Positions
    start_row = problem.start.key.row
    start_col = problem.start.key.col
    avg_goal_row, avg_goal_col = calc_avg_goal_position(problem)

    return {
        'domain': grid.domain,
        'name': grid.name,
        'rows': rows,
        'cols': cols,
        'k': len(problem.goals),
        'dist_start_goals': round(dist_start_goals, 2),
        'nrm_dist_start_goals': round(normalize_dist(dist_start_goals, max_dist), 2),
        'dist_between_goals': round(dist_between_goals, 2),
        'nrm_dist_between_goals': round(normalize_dist(dist_between_goals, max_dist), 2),
        'rlt_start_row': round(calc_relative_position(start_row, rows), 2),
        'rlt_start_col': round(calc_relative_position(start_col, cols), 2),
        'rlt_goal_row': round(calc_relative_position(avg_goal_row, rows), 2),
        'rlt_goal_col': round(calc_relative_position(avg_goal_col, cols), 2),
    }


def problems_to_csv(problems: list[Problem],
                    grids: dict[str, Grid],
                    path_csv: str) -> None:
    """
    ============================================================================
     Convert problems to CSV file.
    ============================================================================
    """
    fieldnames = [
        'domain', 'name', 'rows', 'cols', 'k',
        'dist_start_goals', 'nrm_dist_start_goals',
        'dist_between_goals', 'nrm_dist_between_goals',
        'rlt_start_row', 'rlt_start_col', 'rlt_goal_row', 'rlt_goal_col'
    ]

    with open(path_csv, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for i, problem in enumerate(problems):
            grid_name = problem.grid if isinstance(problem.grid, str) else problem.grid.name
            grid = grids[grid_name]
            row = problem_to_row(problem, grid)
            writer.writerow(row)

            if (i + 1) % 1000 == 0:
                print(f'Processed {i + 1}/{len(problems)} problems')

    print(f'Saved {len(problems)} rows to: {path_csv}')


def main() -> None:
    path_problems = 'f:\\paper\\i_3_problems\\100k\\problems.pkl'
    path_grids = 'f:\\paper\\i_1_grids\\grids.pkl'

    # Derive CSV path from problems path
    path_csv = str(Path(path_problems).with_suffix('.csv'))

    print('Loading grids...')
    grids = load_grids(path_grids)
    print(f'Loaded {len(grids)} grids')

    print('Loading problems...')
    problems = load_problems(path_problems)
    print(f'Loaded {len(problems)} problems')

    print('Converting to CSV...')
    problems_to_csv(problems, grids, path_csv)


if __name__ == '__main__':
    main()