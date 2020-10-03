from f_astar.c_astar import AStar
from f_astar.c_astar_lookup import AStarLookup
from f_map.c_map import Map
from f_utils import u_random


for i in range(10000):
    n = u_random.get_random_int(5, 10)
    map = Map(rows=n, cols=n, obstacles=30)
    start, goal_1, goal_2 = map.get_random_idds(3)
    astar = AStar(map.grid, start, goal_1)
    astar.run()
    if not astar.best:
        continue
    closed_1 = {node.idd for node in astar.closed}
    astar.run(goal_2)
    closed_2 = {node.idd for node in astar.closed}
    set_path_2 = set(astar.get_path())
    d = len(set_path_2 - closed_1)
    forward = len(closed_2 - closed_1)
    if d > forward:
        print(start, goal_1, goal_2)
        print(d, forward)
        print(map.grid)
        break



