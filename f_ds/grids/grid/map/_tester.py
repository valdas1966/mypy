from f_ds.grids.grid.map import GridMap
import numpy as np


def test_neighbors() -> None:
    """
    ========================================================================
     Test the neighbors() method.
    ========================================================================
    """
    grid = GridMap.Factory.x()
    cell_11 = grid[1][1]
    neighbors_11 = grid.neighbors(cell_11)
    assert len(neighbors_11) == 4
    cell_00 = grid[0][0]
    neighbors_00 = grid.neighbors(cell_00)
    assert len(neighbors_00) == 0


def test_cells_valid() -> None:
    """
    ========================================================================
     Test the Cells Valid of the GridMap.
    ========================================================================
    """
    grid = GridMap.Factory.x()
    assert len(grid.cells_valid()) == 5


def test_from_array() -> None:
    """
    ========================================================================
     Test the From.array method.
    ========================================================================
    """
    # Create a boolean np array with a X-Shape
    array = np.array([[True, False, True],
                      [False, True, False],
                      [True, False, True]])
    grid = GridMap.From.array(array)
    assert len(grid.cells_valid()) == 5
