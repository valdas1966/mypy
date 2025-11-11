from f_ds.grids.grid.map import GridMap
import numpy as np


def test_neighbors() -> None:
    """
    ========================================================================
     Test the neighbors() method.
    ========================================================================
    """
    grid = GridMap.Factory.x()
    cell_01 = grid[0][1]
    neighbors_01 = grid.neighbors(cell_01)
    assert len(neighbors_01) == 3
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


def test_from_file_map() -> None:
    """
    ========================================================================
     Test the From.file_map method.
    ========================================================================
    """
    path = 'g:\\temp\\test.txt'
    grid = GridMap.From.file_map(path=path)
    assert len(grid.cells_valid()) == 8


def test_select_random_in_range() -> None:
    """
    ========================================================================
     Test the Select.random_in_range() method.
    ========================================================================
    """
    grid = GridMap.Factory.x()
    selected = grid.select.random_in_range(size=2, row_max=1, col_max=1)
    selected_true = {grid[0][0], grid[1][1]}
    assert set(selected) == selected_true
