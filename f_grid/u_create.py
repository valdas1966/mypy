import random
import numpy as np
from pathlib import Path
from f_grid import u_grid
from f_grid import u_lists
from f_utils import u_tester

"""
================================================================================
 Description: Responsible for Creating Grids.
================================================================================
 Methods:
--------------------------------------------------------------------------------
    1. synthetic(n, percent_obstacles=0) -> Grid
        Return Synthetic Grid by size and percent of obstacles.

    2. from_map(path) -> Grid
        Return Grid derived from Map File.
================================================================================
"""


def synthetic(n, percent_obstacles=0):
    """
    ============================================================================
     Description: Return Synthetic Grid by size and percent of obstacles.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. n : int (Shape of the Grid [n x n]).
        2. percent_obstacles: int
    ============================================================================
     Return: Grid
    ============================================================================
    """
    grid = np.ones([n, n], dtype=int)
    grid = u_grid.serialize(grid)

    if percent_obstacles:
        grid = _add_obstacles(grid, percent_obstacles)

    return grid





"""
================================================================================
================================================================================
==============      Private    =================================================
================================================================================
================================================================================
"""


def _add_obstacles(grid, percent_obstacles):
    """
    ============================================================================
     Description: Add Obstacles (-1) to Grid by percent_obstacles.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. grid : Grid.
        2. percent_obstacles : int
    ============================================================================
     Return: Grid with Obstacles.
    ============================================================================
    """
    len_obstacles = int(grid.size / 100 * percent_obstacles)
    idds = list(range(len_obstacles))
    random.shuffle(idds)
    obstacles = idds[:len_obstacles]
    for obstacle in obstacles:
        row, col = u_grid.to_row_col(grid, obstacle)
        grid[row][col] = -1
    return grid


"""
================================================================================
================================================================================
==============      Tester     =================================================
================================================================================
================================================================================
"""


def tester():

    def tester_add_obstacles():
        grid = np.array([[0, 1], [2, 3]])
        grid = _add_obstacles(grid, 25)
        len_obstacles_test = grid.size - len(u_grid.get_valid_idds(grid))
        len_obstacles_true = 1
        p0 = len_obstacles_test == len_obstacles_true

        u_tester.run([p0])

    def tester_synthetic():
        grid_test = synthetic(3)
        grid_true = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        p0 = np.all(grid_test == grid_true)

        grid_test = synthetic(4, 50)
        len_obstacles_test = grid_test.size - len(u_grid.get_valid_idds(
            grid_test))
        len_obstacles_true = grid_test.size / 2
        p1 = len_obstacles_test == len_obstacles_true

        u_tester.run([p0, p1])

    def tester_from_map():
        path_parent = str(Path(__file__).parent)
        path_map = path_parent + '\\test.map'
        li_1 = 'fgdfg\n'
        li_2 = 'd..l\n'
        li_3 = 'd..\n'
        li = [li_1, li_2, li_3]
        file = open(path_map,'w')
        for i in range(len(li)):
            file.write(li[i])
        file.close()
        grid_test = from_map(path_map)
        grid_true = np.array([[0, 1], [2, 3]])
        p0 = np.all(grid_test == grid_true)

        u_tester.run([p0])

    u_tester.print_start(__file__)
    tester_add_obstacles()
    tester_synthetic()
    tester_from_map()
    u_tester.print_finish(__file__)


if __name__ == '__main__':
    tester()
