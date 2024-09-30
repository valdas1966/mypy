from f_utils.dtypes.inner.list.items import Items
import pytest


def is_even(num: int) -> bool:
    return num % 2 == 0


@pytest.fixture
def ex() -> list:
    return list(range(10))


def test_filter(ex):
    assert Items.filter(li=ex, predicate=is_even) == [0, 2, 4, 6, 8]


def test_sample(ex):
    assert len(Items.sample(li=ex, pct=70)) == 7
