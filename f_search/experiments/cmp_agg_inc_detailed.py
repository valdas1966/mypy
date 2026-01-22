import pandas as pd
from f_utils import u_pickle
from f_psl.pathlib import u_pathlib
from f_search.solutions import SolutionOMSPP


csv_agg_detailed = u_pathlib.to_path('temp/agg_detailed.csv')
csv_inc_detailed = u_pathlib.to_path('temp/inc_detailed.csv')

pickle_aggregative = u_pathlib.to_path('temp/aggregative.pkl')
pickle_incremental = u_pathlib.to_path('temp/incremental.pkl')

li_agg: list[SolutionOMSPP] = u_pickle.load(path=pickle_aggregative)
li_inc: list[SolutionOMSPP] = u_pickle.load(path=pickle_incremental)


def create_detailed_dataframe(solutions: list[SolutionOMSPP]) -> pd.DataFrame:
    """
    Create a detailed DataFrame with overall and per-goal metrics.
    Each row represents one goal from one solution.
    """
    rows = []

    for solution_idx, solution in enumerate(solutions):
        # Overall metrics for this solution
        explored_total = solution.stats.explored
        elapsed_total = solution.stats.elapsed

        # Per-goal metrics
        for goal, sub_solution in solution.subs.items():
            explored_sub = sub_solution.stats.explored
            elapsed_sub = sub_solution.stats.elapsed
            goal_row, goal_col = goal.key.to_tuple()

            rows.append({
                'solution_idx': solution_idx,
                'goal.row': goal_row,
                'goal.col': goal_col,
                'explored_total': explored_total,
                'elapsed_total': elapsed_total,
                'explored_sub': explored_sub,
                'elapsed_sub': elapsed_sub
            })

    return pd.DataFrame(rows)


df_agg_detailed = create_detailed_dataframe(li_agg)
df_inc_detailed = create_detailed_dataframe(li_inc)

df_agg_detailed.to_csv(csv_agg_detailed, index=False)
df_inc_detailed.to_csv(csv_inc_detailed, index=False)
