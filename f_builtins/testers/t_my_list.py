from f_builtins.my_list import MyList
import pytest


@pytest.fixture
def ex() -> MyList:
    return MyList([1, 2, 3])


def test_move(ex):
    ex.move(item=3, index=1)
    assert ex == [1, 3, 2]


def test_replace(ex):
    ex.replace(d={2: 5})
    assert ex == [1, 5, 3]
