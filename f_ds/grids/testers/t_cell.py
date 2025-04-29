from f_ds.grids.generators.g_cell import GenCell, Cell


def test_zero() -> None:
    """
    ============================================================================
     Test the zero method.
    ============================================================================
    """
    cell = GenCell.zero()
    assert cell.row == 0
    assert cell.col == 0
    assert cell
    cell.set_invalid()
    assert not cell


def test_distance() -> None:
    """
    ============================================================================
     Test the distance method.
    ============================================================================
    """
    cell_a = GenCell.zero()
    cell_b = GenCell.one()
    assert cell_a.distance(cell_a) == 0
    assert cell_a.distance(cell_b) == 2


def test_farthest() -> None:
    """
    ============================================================================
     Test the farthest method.
    ============================================================================
    """
    zero = GenCell.zero()
    one = GenCell.one()
    cells = [zero, one]
    assert zero.farthest(cells) == one
    
