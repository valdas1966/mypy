from f_ds.grids.cell.i_0_base.main import CellBase


def test_str() -> None:
    """
    ========================================================================
     Test the __str__() method.
    ========================================================================
    """
    cell = CellBase.Factory.zero()
    assert str(cell) == 'CellBase(0,0)'


def test_repr() -> None:
    """
    ========================================================================
     Test the __repr__() method.
    ========================================================================
    """
    cell = CellBase.Factory.zero()
    assert repr(cell) == '<CellBase: Name=CellBase, Row=0, Col=0>'
