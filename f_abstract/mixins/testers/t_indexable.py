import pytest
from f_abstract.mixins.indexable import Indexable


@pytest.fixture
def ex() -> Indexable:
    class Sub(Indexable[int]):
        def to_list(self) -> list[int]:
            return [1, 2, 3]
    return Sub()


def test_current(ex):
    ex.next()
    assert ex.current() == 1


def test_has_next(ex):
    assert ex.has_next()
    ex.next()
    ex.next()
    ex.next()
    assert not ex.has_next()


def test_next(ex):
    assert ex.next() == 1
