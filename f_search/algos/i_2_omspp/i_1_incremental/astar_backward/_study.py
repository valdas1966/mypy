from f_search.algos.i_2_omspp.i_1_incremental import AStarIncrementalBackward
from f_search.problems.i_2_omspp import ProblemOMSPP
import pandas as pd


def analyze_explored() -> None:
    problem = ProblemOMSPP.Factory.for_cached()
    algo = AStarIncrementalBackward(problem=problem, is_analytics=True, with_bounds=True)
    algo.run()
    list_explored = algo.list_explored()
    df = pd.DataFrame(list_explored)
    df.to_csv('f:\\temp\\2026\\03\\explored.csv', index=False)


def analyze_bounded() -> None:
    problem = ProblemOMSPP.Factory.for_cached()
    algo = AStarIncrementalBackward(problem=problem,
                                    is_analytics=True,
                                    with_bounds=True)
    algo.run()
    rows = list()
    for goal, bounded in algo.dict_bounded_per_goal().items():
        for state, bound in bounded.items():
            rows.append({'goal_row': goal.key.row,
                         'goal_col': goal.key.col,
                         'state_row': state.key.row,
                         'state_col': state.key.col,
                         'bound': bound})
    df = pd.DataFrame(rows)
    df.to_csv('f:\\temp\\2026\\03\\bounded.csv', index=False)


analyze_bounded()
