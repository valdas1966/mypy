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
