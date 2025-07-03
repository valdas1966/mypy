from f_ds.grids.cell.map.main import CellMap


def test_valid() -> None:
    """
    ========================================================================
     Test the valid-property of the CellMap.
    ========================================================================
    """
    cell = CellMap.Factory.zero()
    assert cell
    cell.set_invalid()
    assert not cell
