import pytest
from f_hs.state.i_1_cell import StateCell


@pytest.fixture
def a() -> StateCell:
    """
    ========================================================================
     Create a StateCell at (0, 0).
    ========================================================================
    """
    return StateCell.Factory.a()


@pytest.fixture
def b() -> StateCell:
    """
    ========================================================================
     Create a StateCell at (2, 2).
    ========================================================================
    """
    return StateCell.Factory.b()


def test_key(a: StateCell) -> None:
    """
    ========================================================================
     Test the key property returns the CellMap.
    ========================================================================
    """
    assert a.key.row == 0
    assert a.key.col == 0


def test_distance(a: StateCell, b: StateCell) -> None:
    """
    ========================================================================
     Test Manhattan distance between two StateCells.
    ========================================================================
    """
    assert a.distance(b) == 4


def test_eq(a: StateCell) -> None:
    """
    ========================================================================
     Test equality between two StateCells at the same position.
    ========================================================================
    """
    other = StateCell.Factory.a()
    assert a == other


def test_neq(a: StateCell, b: StateCell) -> None:
    """
    ========================================================================
     Test inequality between two StateCells at different positions.
    ========================================================================
    """
    assert a != b


def test_hash(a: StateCell) -> None:
    """
    ========================================================================
     Test hash consistency with equality.
    ========================================================================
    """
    other = StateCell.Factory.a()
    assert hash(a) == hash(other)


def test_str(a: StateCell) -> None:
    """
    ========================================================================
     Test string representation.
    ========================================================================
    """
    assert str(a) == 'CellMap(0,0)'
