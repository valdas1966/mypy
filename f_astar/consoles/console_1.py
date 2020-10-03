# Feature Extraction from A* (before backward search)

from f_utils import u_pickle
from f_map.c_map import Map


path_astars = 'D:\\MyPy\\astars'
path_example = path_astars + '\\arena.map_00.pickle'


astar = u_pickle.load(path_example)
map = Map(grid=astar.grid)
shape = map.shape
offsets_start = map.offsets(astar.start)
offsets_goal_near = map.offsets(astar.goal)
distance_start_goal_near = map.distance(astar.start, astar.goal)
len_closed = len(astar.closed)
ratio_closed = len_closed / distance_start_goal_near



