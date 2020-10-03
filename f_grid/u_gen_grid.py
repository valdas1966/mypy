import random as rand
import numpy as np
from f_grid import u_grid
from f_grid import u_lists


def random(rows, cols=None, obstacles=None):
    """
    ============================================================================
     Description: Generate serialized Grid with random Obstacles.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. rows : int (Total Rows).
        2. cols : int (Total Cols - equal to rows if cols is None).
        3. obstacles : float (Percent of Obstacles in the Grid).
    ============================================================================
     Return: Grid.
    ============================================================================
    """
    if not cols:
        cols = rows
    grid = np.ones([rows, cols], dtype=int)
    grid = u_grid.serialize(grid)
    if not obstacles:
        return grid
    amount_idds = rows * cols
    amount_obstacles = int(amount_idds // (100 / obstacles))
    idds = list(range(amount_idds))
    rand.shuffle(idds)
    li_obstacles = idds[:amount_obstacles]
    for obstacle in li_obstacles:
        row, col = u_grid.to_row_col(grid, obstacle)
        grid[row][col] = -1
    return grid


def from_map(path):
    """
    ============================================================================
     Description: Return Canonized Grid derived from Map File.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. path : str (Path to the Map File).
    ============================================================================
     Return: Canonized Grid.
    ============================================================================
    """
    lists = u_lists.to_lists_mask(path, '.')
    grid = u_grid.lists_to_grid(lists)
    return u_grid.canonize(grid)