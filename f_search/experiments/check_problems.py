from f_utils import u_pickle
from pathlib import Path
from typing import Sequence
import csv


def _max_pairwise_manhattan(goals) -> int:
    """
    Max Manhattan distance among (row,col) goals in O(k):
      max |r1-r2|+|c1-c2| = max( max(r+c)-min(r+c), max(r-c)-min(r-c) )
    """
    k = len(goals)
    if k < 2:
        return 0

    s0 = goals[0].key.row + goals[0].key.col
    d0 = goals[0].key.row - goals[0].key.col

    s_min = s_max = s0
    d_min = d_max = d0

    for g in goals[1:]:
        s = g.key.row + g.key.col
        d = g.key.row - g.key.col
        if s < s_min: s_min = s
        if s > s_max: s_max = s
        if d < d_min: d_min = d
        if d > d_max: d_max = d

    return max(s_max - s_min, d_max - d_min)


def write_omspps_csv(
    problems: Sequence,  # Sequence[ProblemOMSPP]
    csv_path: str | Path,
) -> Path:
    """
    Column order:
      problem_index, grid, start_row, start_col, num_goals, max_goal_goal_dist,
      goal_1_row, goal_1_col, ..., goal_k_row, goal_k_col
    where k = max number of goals among problems (pad shorter ones with empty cells).
    """
    csv_path = Path(csv_path)

    # Determine k across the whole list
    max_k = 0
    for p in problems:
        if not hasattr(p, "goals"):
            raise AttributeError("Problem is missing `.goals`.")
        max_k = max(max_k, len(p.goals))

    # Header in the exact order you requested
    header = [
        "problem_index",
        "grid",
        "start_row",
        "start_col",
        "num_goals",
        "max_goal_goal_dist",
    ]
    for i in range(1, max_k + 1):
        header += [f"goal_{i}_row", f"goal_{i}_col"]

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)

        for idx, p in enumerate(problems):
            grid_str = str(p._grid)
            start = p.start
            goals = p.goals

            num_goals = len(goals)
            max_dist = _max_pairwise_manhattan(goals)

            row = [
                idx,
                grid_str,
                start.key.row,
                start.key.col,
                num_goals,
                max_dist,
            ]

            # Goals
            for g in goals:
                row.append(g.key.row)
                row.append(g.key.col)

            # Pad missing goals (2 cells each)
            missing = max_k - num_goals
            if missing > 0:
                row.extend([""] * (2 * missing))

            w.writerow(row)

    return csv_path


# Example:
# out = write_omspps_csv(list_of_problems, "omspp.csv")
# print("Wrote:", out)

path_pickle = 'f:\\paper\\i_3_problems\\problems.pkl'
path_csv = 'f:\\paper\\i_3_problems\\problems.csv'

problems: list = u_pickle.load(path=path_pickle)
out = write_omspps_csv(problems, path_csv)
print("Wrote:", out)
