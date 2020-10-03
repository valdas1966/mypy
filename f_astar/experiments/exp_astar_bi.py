import pandas as pd
from f_utils import u_pickle
from f_utils import u_list
from f_astar.c_astar_bi import AStarBi
from f_astar.c_astar import AStar

path_assymetry = 'D:\\MyPy\\f_astar\\experiments\\results_astar_assymetry.csv'
path_results = 'D:\\MyPy\\f_astar\\experiments\\results_astar_bi.csv'
pickle_maps = 'D:\\MyPy\\f_map\\maps\\maps.pickle'

maps = u_pickle.load(pickle_maps)

file = open(path_results, 'w')
titles = 'i,map,width,height,start,start_up,start_right,start_down,start_left,'
titles += 'goal,goal_up,goal_right,goal_down,goal_left,top,left,'
titles += 'distance,forward,backward,astar_bi\n'
file.write(titles)
file.close()
df = pd.read_csv(path_assymetry)
for index, row in df.iterrows():
    m = row['map']
    if m == 'brc000d':
        continue
    start = row['start']
    goal = row['goal']
    grid = maps[m].grid
    astar_bi = AStarBi(grid, start, goal)
    astar_bi.run()
    bi = astar_bi.expanded_nodes
    line = f'{u_list.to_str(row.values)},{bi}\n'
    file = open(path_results, 'a')
    file.write(line)
    file.close()
    print(index)
