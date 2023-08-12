import pytest
from f_data_structure.mixins.xyable import XYAble
from f_data_structure.old_grid_cells import GridCells
from f_data_structure.old_cell import Cell


@pytest.fixture
def grid():
    """
    ========================================================================
     Desc: Pytest fixture that returns a 10x10 grid with 30% obstacles
            for testing.
    ========================================================================
    """
    return GridCells(rows=10, percentage_obstacle=30)


def test_init(grid):
    assert isinstance(grid, GridCells)
    assert grid.rows == 10
    assert grid.cols == 10
    assert grid.percentage_obstacle == 30


def test_set_obstacles(grid):
    assert grid.count_elements == 70
    assert grid.count_obstacles == 30


def test_elements(grid):
    assert all(isinstance(cell, Cell) for cell in grid.elements())


def test_neighbors(grid):
    xy = XYAble(0, 0)
    grid[0][1].is_valid = False
    grid[1][0].is_valid = True
    expected = [Cell(1, 0)]
    assert xy.neighbors() == expected


def test_is_valid(grid):
    grid[0][0].is_valid = True
    grid[1][1].is_valid = False
    assert grid.is_valid(x=0, y=0)
    assert not grid.is_valid(x=1, y=1)
    xy_1 = XYAble(0, 0)
    xy_2 = XYAble(1, 1)
    assert grid.is_valid(xy=xy_1)
    assert not grid.is_valid(xy=xy_2)
