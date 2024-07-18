import pytest
from f_abstract.components.position import Position


@pytest.fixture
def ex() -> Position:
    pos = Position()
    pos.relative = (50, 50, 50, 50)
    pos.update(200, 300)
    return pos


def test_update(ex) -> None:
    assert ex.absolute == (100, 150, 100, 150)


def test_str(ex) -> None:
    assert str(ex) == '(50%, 50%, 50%, 50%) * (200x300) -> (100, 150, 100, 150)'
