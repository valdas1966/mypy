import pytest
from f_abstract.mixins.iterable import Iterable, Item


@pytest.fixture
def ex_empty() -> Iterable:
    class Sub(Iterable):
        def to_list(self) -> list[Item]:
            return []
    return Sub()


@pytest.fixture
def ex_full() -> Iterable:
    class Sub(Iterable):
        def to_list(self) -> list[Item]:
            return [1, 2, 3]
    return Sub()


def test_insert(ex_full):
    ex_full.insert(4, 1)
    assert list(ex_full) == [1, 4, 2, 3]


def test_iter(ex_empty, ex_full):
    assert list(ex_empty) == []
    assert list(ex_full) == [1, 2, 3]


def test_len(ex_empty, ex_full):
    assert len(ex_empty) == 0
    assert len(ex_full) == 3


def test_bool(ex_empty, ex_full):
    assert not ex_empty
    assert ex_full


def test_contains(ex_empty, ex_full):
    assert 1 not in ex_empty
    assert 1 in ex_full


def test_str(ex_empty, ex_full):
    assert str(ex_empty) == '[]'
    assert str(ex_full) == '[1, 2, 3]'
