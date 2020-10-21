from f_map.c_point import Point
from f_map.c_grid import Grid
from f_utils import u_random


def blocks(rows, cols, percent_blocks):
    """
    ========================================================================
     Description: Constructor.
    ========================================================================
     Arguments:
    ------------------------------------------------------------------------
        1. rows : int
        2. cols : int
        3. percent_blocks : int (Percent of Blocks in the Map [0:100])
    ========================================================================
    """
    len_blocks = int(rows * cols * percent_blocks / 100)
    points_blocks = set()
    while len(points_blocks) < len_blocks:
        x = u_random.randint(0, rows-1)
        y = u_random.randint(0, cols-1)
        points_blocks.add(Point(x, y))
    grid = Grid(rows, cols)
    for point in points_blocks:
        grid.set_block(point=point)
    return grid


