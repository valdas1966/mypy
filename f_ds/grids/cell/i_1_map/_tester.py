from f_ds.grids.cell.i_1_map.main import CellMap


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

def test_eq() -> None:
    zero = CellMap.Factory.zero()
    zero_other = CellMap.Factory.zero()
    assert zero == zero_other
    one = CellMap.Factory.one()
    assert one != zero
