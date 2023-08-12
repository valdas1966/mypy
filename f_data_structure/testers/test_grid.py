import pytest
from f_data_structure.mixins.xyable import XYAble
from f_data_structure.grid import Grid


@pytest.fixture
def grid():
    """
    ========================================================================
     Desc: Pytest fixture that returns a 3x3 grid for testing.
    ========================================================================
    """
    return Grid(rows=3)


def test_shape(grid):
    """
    ========================================================================
     Desc: Test that the grid's shape is correctly reported.
    ========================================================================
    """
    assert grid.shape() == "(3,3)", "The shape should be (3,3)."


def test_elements(grid):
    """
    ========================================================================
     Desc: Test that all elements in the grid are instances of XYAble.
    ========================================================================
    """
    elements = grid.elements()
    assert isinstance(elements, list)
    assert len(elements) == grid.rows * grid.cols
    assert all(isinstance(ele, XYAble) for ele in elements),\
        "All elements should be instances of XYAble."


def test_neighbors(grid):
    xy = XYAble(0, 2)
    expected = [XYAble(1, 2), XYAble(0, 1)]
    assert grid.neighbors(xy) == expected


def test_is_valid(grid):
    """
    ========================================================================
     Desc: Test that is_valid returns True for valid coordinates
           and False for invalid ones.
    ========================================================================
    """
    assert grid.is_valid(1, 1), "Coordinates (1,1) should be valid."
    assert not grid.is_valid(3, 3), "Coordinates (3,3) should be invalid."
    assert not grid.is_valid(-1, 0), "Coordinates (-1,0) should be invalid."
    xy_1 = XYAble(2, 2)
    xy_2 = XYAble(4, 4)
    assert grid.is_valid(xy=xy_1)
    assert not grid.is_valid(xy=xy_2)


def test_get_item(grid):
    """
    ========================================================================
     Desc: Test that grid elements can be accessed via indexing.
    ========================================================================
    """
    row = grid[1]
    assert isinstance(row, list), "The row should be a list."
    assert all(isinstance(ele, XYAble) for ele in row),\
        "All elements should be instances of XYAble."
    xyable = grid[1][2]
    assert xyable.x == 1 and xyable.y == 2


def test_rows_and_cols(grid):
    """
    ========================================================================
     Desc: Test that the grid's rows and columns properties are correctly reported.
    ========================================================================
    """
    assert grid.rows == 3, "The number of rows should be 3."
    assert grid.cols == 3, "The number of columns should be 3."
