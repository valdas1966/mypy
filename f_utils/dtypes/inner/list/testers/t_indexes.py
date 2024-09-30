from f_utils.dtypes.inner.list.indexes import Indexes
import pytest


@pytest.fixture
def ex() -> list[int]:
    return [1, 0, 1]


def test_filter(ex):
    assert Indexes.filter(li=ex, predicate=bool) == [0, 2]


def test_sample(ex):
    assert set(Indexes.sample(li=ex, pct=100)) == {0, 1, 2}
