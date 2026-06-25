from f_ds.grids.connectivity.i_0_base.main import ConnectivityBase
from f_ds.grids.cell import CellMap


def test_unit() -> None:
    """
    ========================================================================
     Test the default unit is 1.
    ========================================================================
    """
    connectivity = ConnectivityBase()
    assert connectivity.unit == 1


def test_is_legal_move() -> None:
    """
    ========================================================================
     Test the default is_legal_move always returns True.
    ========================================================================
    """
    connectivity = ConnectivityBase()
    a = CellMap(row=0, col=0)
    b = CellMap(row=1, col=1)
    is_free = lambda row, col: True
    assert connectivity.is_legal_move(a=a, b=b, is_free=is_free) is True
