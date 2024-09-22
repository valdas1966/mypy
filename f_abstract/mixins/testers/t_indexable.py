import pytest
from f_abstract.mixins.indexable import Indexable


@pytest.fixture
def ex() -> Indexable:
    return Indexable(items=[1, 2, 3])


def test_insert_at(ex) -> None:
    ex.insert_at(item=4, index=1)
    assert list(ex) == [1, 4, 2, 3]


def test_insert_of(ex) -> None:
    assert ex.index_of(item=2) == 1
