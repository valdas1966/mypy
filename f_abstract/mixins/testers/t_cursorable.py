from f_abstract.mixins.cursorable import Cursorable
import pytest


@pytest.fixture
def ex() -> Cursorable:
    data = [1, 2, 3]
    return Cursorable(data=data)


def test_cursor(ex):
    assert ex.cursor == 0


def test_current(ex):
    assert ex.current() == 1


def test_advance(ex):
    ex.advance()
    assert ex.cursor == 1
    ex.advance(times=3)
    assert ex.cursor == 4


def test_has_next(ex):
    assert ex.has_next()
    ex.advance(times=3)
    assert not ex.has_next()


def test_next(ex):
    assert ex.next() == 2


def test_to_list(ex):
    assert ex.to_list() == [1, 2, 3]

