import pandas as pd
from f_utils import u_pickle
from f_psl.pathlib import u_pathlib
from f_search.solutions import SolutionOMSPP


csv_agg = u_pathlib.to_path('temp/agg.csv')
csv_inc = u_pathlib.to_path('temp/inc.csv')

pickle_aggregative = u_pathlib.to_path('temp/aggregative.pkl')
pickle_incremental = u_pathlib.to_path('temp/incremental.pkl')

li_agg: list[SolutionOMSPP] = u_pickle.load(path=pickle_aggregative)
li_inc: list[SolutionOMSPP] = u_pickle.load(path=pickle_incremental)

li_agg_explored = [solution.stats.explored for solution in li_agg]
li_agg_elapsed = [solution.stats.elapsed for solution in li_agg]
li_inc_explored = [solution.stats.explored for solution in li_inc]
li_inc_elapsed = [solution.stats.elapsed for solution in li_inc]

df_agg = pd.DataFrame({'explored': li_agg_explored, 'elapsed': li_agg_elapsed})
df_inc = pd.DataFrame({'explored': li_inc_explored, 'elapsed': li_inc_elapsed})

df_agg.to_csv(csv_agg, index=False)
df_inc.to_csv(csv_inc, index=False)
