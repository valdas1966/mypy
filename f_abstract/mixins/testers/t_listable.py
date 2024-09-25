from f_abstract.mixins.listable import Listable
import pytest


@pytest.fixture
def ex_1() -> Listable:
    data = [1, 2, 3]
    return Listable(data=data)

@pytest.fixture
def ex_2() -> Listable:
    data = [4, 5]
    return Listable(data=data)


def test_move(ex_1):
    ex_1.move(item=2, index=0)
    assert list(ex_1) == [2, 1, 3]


def test_add(ex_1, ex_2):
    ex = ex_1 + ex_2
    assert ex == [1, 2, 3, 4, 5]
    