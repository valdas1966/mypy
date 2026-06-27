from f_hs.state import StateCell as State
from f_ds.grids import CellMap as Cell


def test_key() -> None:
    """
    ========================================================================
     Test the key property returns the CellMap.
    ========================================================================
    """
    zero = State.Factory.at(row=0)
    assert zero.key == Cell.Factory.at(row=0)
