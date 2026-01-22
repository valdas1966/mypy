import pandas as pd
from f_utils import u_pickle
from f_psl.pathlib import u_pathlib
from f_search.problems import ProblemOMSPPLite as ProblemLite


pickle_problems = u_pathlib.to_path('temp/problems.pkl')
csv_problems = u_pathlib.to_path('temp/problems.csv')

problems: list[ProblemLite] = u_pickle.load(path=pickle_problems)

# Find the maximum number of goals across all problems
max_goals = max(len(problem.goals) for problem in problems)

# Create rows for the dataframe
rows = []
for idx, problem in enumerate(problems):
    row = {
        'index': idx,
        'grid.name': problem.grid,
        'start.row': problem.start.key.to_tuple()[0],
        'start.col': problem.start.key.to_tuple()[1]
    }

    # Add goal columns
    for goal_idx, goal in enumerate(problem.goals, start=1):
        goal_row, goal_col = goal.key.to_tuple()
        row[f'goal_{goal_idx}.row'] = goal_row
        row[f'goal_{goal_idx}.col'] = goal_col

    # Fill remaining goal columns with None for problems with fewer goals
    for goal_idx in range(len(problem.goals) + 1, max_goals + 1):
        row[f'goal_{goal_idx}.row'] = None
        row[f'goal_{goal_idx}.col'] = None

    rows.append(row)

df_problems = pd.DataFrame(rows)
df_problems.to_csv(csv_problems, index=False)
