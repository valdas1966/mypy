import random
from f_grid import u_create
from f_grid import u_grid
from f_astar.c_astar import AStar

path_map = 'D:\\MyPy\\f_astar\\ost000a.map'
path_results = 'D:\\MyPy\\f_astar\\results1.csv'

d = dict()
for i in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
    d[i] = 0
file = open(path_results, 'r')
for i, line in enumerate(file):
    if i == 0:
        continue
    forward = int(line.split(',')[3])
    backward = int(line.split(',')[4])
    ratio = round(min(forward, backward) / max(forward, backward), 1)
    d[ratio] += 1
file.close()
for key in sorted(d.keys()):
    print(key, d[key])

"""
grid = u_create.from_map(path_map)
idds = u_grid.get_valid_idds(grid)
file = open(path_results, 'a')
file.write('start, goal, distance, forward, backward, path_forward, '
           'path_backward\n')
for i in range(1000):
    print(i)
    random.shuffle(idds)
    start = idds[0]
    goal = idds[1]
    distance = u_grid.manhattan_distance(grid, start, goal)
    astar_fore = AStar(grid, start, goal)
    astar_back = AStar(grid, goal, start)
    len_fore = len(astar_fore.closed)
    len_back = len(astar_back.closed)
    path_fore = len(astar_fore.get_path())
    path_back = len(astar_back.get_path())
    file = open(path_results, 'a')
    file.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(start, goal, distance,
                                                      len_fore, len_back,
                                                      path_fore, path_back))
    file.close()
"""