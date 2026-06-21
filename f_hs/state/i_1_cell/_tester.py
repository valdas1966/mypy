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


def test_distance() -> None:
    """
    ========================================================================
     Test Manhattan distance between two StateCells.
    ========================================================================
    """
    zero = State.Factory.at(row=0)
    one = State.Factory.at(row=1)
    assert zero.distance(zero) == 0
    assert zero.distance(one) == 2
