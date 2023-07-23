import pytest
from f_data_structure.inner.xy.i_1_order import XYOrder


@pytest.fixture
def objects():
    o_1 = XYOrder(0, 0)
    o_2 = XYOrder(1, 0)
    o_3 = XYOrder(0, 1)
    return o_1, o_2, o_3


def test_lt(objects):
    o_1, o_2, o_3 = objects
    assert not o_1 < o_1
    assert o_1 < o_2
    assert o_2 < o_3


def test_gt(objects):
    o_1, o_2, o_3 = objects
    assert not o_1 > o_1
    assert o_2 > o_1
    assert o_3 > o_2


def test_le(objects):
    o_1, o_2, o_3 = objects
    assert o_1 <= o_1
    assert o_1 <= o_2
    assert o_2 <= o_3


def test_ge(objects):
    o_1, o_2, o_3 = objects
    assert o_1 >= o_1
    assert o_2 >= o_1
    assert o_3 >= o_2
