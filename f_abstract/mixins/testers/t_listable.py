from f_abstract.mixins.listable import Listable
import pytest


@pytest.fixture
def ex() -> Listable:
    data = [1, 2, 3]
    return Listable(data=data)


def test_move(ex):
    ex.move(item=2, index=0)
    assert list(ex) == [2, 1, 3]

