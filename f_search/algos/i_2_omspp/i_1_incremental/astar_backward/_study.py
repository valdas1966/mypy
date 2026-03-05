from f_search.algos.i_2_omspp.i_1_incremental import AStarIncrementalBackward
from f_search.problems.i_2_omspp import ProblemOMSPP
import pandas as pd


problem = ProblemOMSPP.Factory.for_cached()
algo = AStarIncrementalBackward(problem=problem, is_analytics=True, depth_propagation=0)
sol = algo.run()
list_explored = algo.list_explored()
df = pd.DataFrame(list_explored)
df.to_csv('explored.csv')
