from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence
import csv

from f_utils import u_pickle


# ----------------------------
# Robust coordinate extraction
# ----------------------------

def _row_col(obj: Any) -> tuple[int, int]:
    """
    Extract (row, col) from:
      - CellMap-like objects that have .row and .col
      - StateCell-like objects that have .key (possibly nested)
      - tuples: (row, col)
    """
    # tuple (row, col)
    if isinstance(obj, tuple) and len(obj) == 2:
        r, c = obj
        return int(r), int(c)

    # unwrap .key chains until we see .row/.col
    x = obj
    seen = 0
    while True:
        # direct row/col
        if hasattr(x, "row") and hasattr(x, "col"):
            return int(getattr(x, "row")), int(getattr(x, "col"))

        # unwrap State-like .key
        if hasattr(x, "key"):
            x = getattr(x, "key")
            seen += 1
            if seen > 10:
                # avoid infinite loops in weird objects
                raise TypeError(f"Too many `.key` unwraps; cannot get (row,col) from {type(obj).__name__}")
            continue

        raise TypeError(f"Cannot extract (row,col) from {type(obj).__name__}: {obj!r}")


# ----------------------------
# Max pairwise Manhattan (O(k))
# ----------------------------

def _max_pairwise_manhattan(goals: Sequence[Any]) -> int:
    """
    Max Manhattan distance among goals, where each goal can be State/Cell/tuple.
    O(k) using:
      max |r1-r2|+|c1-c2| = max( max(r+c)-min(r+c), max(r-c)-min(r-c) )
    """
    k = len(goals)
    if k < 2:
        return 0

    r0, c0 = _row_col(goals[0])
    s0 = r0 + c0
    d0 = r0 - c0

    s_min = s_max = s0
    d_min = d_max = d0

    for g in goals[1:]:
        r, c = _row_col(g)
        s = r + c
        d = r - c

        if s < s_min:
            s_min = s
        if s > s_max:
            s_max = s
        if d < d_min:
            d_min = d
        if d > d_max:
            d_max = d

    return max(s_max - s_min, d_max - d_min)


# ----------------------------
# CSV writer
# ----------------------------

def write_omspps_csv(
    problems: Sequence[Any],  # Sequence[ProblemOMSPP]
    csv_path: str | Path,
) -> Path:
    """
    Column order:
      problem_index, grid, start_row, start_col, num_goals, max_goal_goal_dist,
      goal_1_row, goal_1_col, ..., goal_k_row, goal_k_col
    where k = max number of goals among problems (pad shorter ones with empty cells).
    """
    csv_path = Path(csv_path)

    # Determine max_k across all problems
    max_k = 0
    for p in problems:
        if not hasattr(p, "goals"):
            raise AttributeError(f"{type(p).__name__} is missing `.goals`.")
        max_k = max(max_k, len(p.goals))

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
            # grid could be a Grid object or a grid-name string; we just stringify it
            grid_str = str(getattr(p, "_grid", getattr(p, "grid", "")))

            start = getattr(p, "start", None)
            if start is None:
                raise AttributeError(f"{type(p).__name__} is missing `.start`.")

            goals = p.goals
            num_goals = len(goals)

            start_r, start_c = _row_col(start)
            max_dist = _max_pairwise_manhattan(goals)

            row: list[Any] = [
                idx,
                grid_str,
                start_r,
                start_c,
                num_goals,
                max_dist,
            ]

            # goals coords
            for g in goals:
                r, c = _row_col(g)
                row.append(r)
                row.append(c)

            # pad missing goals
            missing = max_k - num_goals
            if missing > 0:
                row.extend([""] * (2 * missing))

            w.writerow(row)

    return csv_path


# ----------------------------
# Main
# ----------------------------

if __name__ == "__main__":
    path_pickle = r"f:\paper\i_3_problems\problems - 100k.pkl"
    path_csv = r"f:\paper\i_3_problems\problems.csv"

    problems: list[Any] = u_pickle.load(path=path_pickle)
    out = write_omspps_csv(problems, path_csv)
    print("Wrote:", out)
