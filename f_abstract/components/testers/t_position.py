import pytest
from f_abstract.components.ltwh import LTWH
from f_abstract.components.position import Position


@pytest.fixture
def ex() -> Position:
    pos = Position()
    pos.relative = (0.5, 0.5, 0.5, 0.5)
    pos.parent = LTWH(0, 0, 50, 50)
    return pos


@pytest.fixture
def ex_2() -> Position:
    pos = Position()
    pos.relative = (0, 0, 1, 1)
    pos.parent = LTWH(0, 0, 100, 100)
    return pos


def test_update(ex, ex_2) -> None:
    assert ex.absolute.values == (25, 25, 25, 25)
    assert ex_2.absolute.values == (0, 0, 100, 100)


def test_str(ex) -> None:
    assert str(ex) == '(0.5, 0.5, 0.5, 0.5) X (0, 0, 50, 50) -> (25, 25, 25, 25)'
