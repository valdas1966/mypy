from f_utils import u_pickle
from f_utils import u_file
from f_grid import u_grid
import pandas as pd


path_results = 'G:\\MyPy\\f_astar\\experiments\\results_kastar_lookup_3.csv'
path_astars = 'G:\\MyPy\\astars_3\\'
path_d = 'G:\\MyPy\\f_astar\\experiments\\d.csv'

li_i = list()
li_d = list()
df = pd.read_csv(path_results)
for i, filepath in enumerate(u_file.filepaths(path_astars)):
    astar = u_pickle.load(filepath)
    goal_far = int(df.at[i, 'goal_far'])
    path_old = {node.idd for node in astar.closed}
    astar.run(goal_far)
    path_new = set(astar.get_path())
    d = len(path_new - path_old)
    li_i.append(i)
    li_d.append(len(path_new))
    print(i)
df_d = pd.DataFrame({'i': li_i, 'd': li_d})
df_d.to_csv(path_d)
