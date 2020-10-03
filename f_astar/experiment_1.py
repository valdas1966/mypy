from pathlib import Path
path_parent = str(Path(Path(Path(__file__).parent).parent))

import sys
sys.path.append(path_parent + '\\f_utils')
sys.path.append(path_parent + '\\f_grid')
import u_grid
import u_lists
import u_map

from c_kastar import KAStar
from c_kastar_h import KAStar_H

import random

path_map = 'D:\\MyPy\\f_astar\\ost000a.map'
path_results = 'D:\\MyPy\\f_astar\\results.csv'

lists = u_lists.to_lists_mask(path_map,'.')
grid = u_grid.lists_to_grid(lists)
grid = u_grid.canonize(grid)
idds = u_grid.get_valid_idds(grid)

file = open(path_results,'w')
for k in [2,5,10,20,50,100]:
    counter = 0
    while counter < 100:
        count_kastar = 0
        count_kastar_h = 0
        random.shuffle(idds)
        start = idds[0]
        goals = idds[1:k+1]
        kastar = KAStar(grid, start, goals)
        kastar.run()
        kastar_h = KAStar_H(grid, start, goals)
        kastar_h.run()
        if not kastar_h.has_solution:
            continue
        counter += 1
        if counter % 10 == 0:
            print('{0}, {1}%'.format(k, counter))
        file.write('{0},{1},{2},{3}\n'.format(k,counter,count_kastar,count_kastar_h))
file.close()