from f_core.mixins.cursorable import Cursorable
import pytest


@pytest.fixture
def ex() -> Cursorable:
    data = [1, 2, 3]
    return Cursorable(data=data)


def test_cursor(ex):
    assert ex.cursor() == -1
    ex.advance()
    assert ex.cursor() == 0


def test_current(ex):
    assert ex.current() is None
    ex.advance()
    assert ex.current() == 1


def test_advance(ex):
    ex.advance()
    assert ex.cursor() == 0
    ex.advance(times=3)
    assert ex.cursor() == 3


def test_retreat(ex):
    ex.advance(times=2)
    ex.retreat()
    assert ex.cursor() == 0


def test_has_next(ex):
    assert ex.has_next()
    ex.advance(times=3)
    assert not ex.has_next()


def test_has_prev(ex):
    assert not ex.has_prev()
    ex.advance()
    assert ex.has_prev()


def test_next(ex):
    assert ex.next() == 1


def test_prev(ex):
    ex.advance(times=2)
    assert ex.prev() == 1


def test_peek_prev(ex):
    ex.advance(2)
    assert ex.peek_prev() == 1
    assert ex.cursor() == 1


def test_peek_next(ex):
    assert ex.peek_next() == 1
    assert ex.cursor() == -1
