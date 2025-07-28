from f_ds.grids.grid.base.main import GridBase


def test_neighbors() -> None:
    """
    ========================================================================
     Test the neighbors() method.
    ========================================================================
    """ 
    grid = GridBase.Factory.grid_3x3()
    cell_11 = grid[1][1]
    neighbors_11 = grid.neighbors(cell_11)
    assert len(neighbors_11) == 4
    cell_00 = grid[0][0]
    neighbors_00 = grid.neighbors(cell_00)
    assert len(neighbors_00) == 2
    
    
def test_len() -> None:
    """
    ========================================================================
     Test the Length of the Grid.
    ========================================================================
    """
    grid = GridBase.Factory.grid_3x3()
    assert len(grid) == 9


def test_list() -> None:
    """
    ========================================================================
     Test the List of the Grid.
    ========================================================================
    """
    grid = GridBase.Factory.grid_3x3()
    cells = list(grid)
    assert len(cells) == 9


def test_group() -> None:
    """
    ========================================================================
     Test the Group of the Grid.
    ========================================================================
    """
    grid = GridBase.Factory.grid_3x3()
    sampled = grid.sample(size=3)
    assert len(sampled) == 3


def test_getitem() -> None:
    """
    ========================================================================
     Test the Get Item of the Grid.
    ========================================================================
    """
    grid = GridBase.Factory.grid_3x3()
    cell = grid[1][2]
    assert cell.row == 1
    assert cell.col == 2

