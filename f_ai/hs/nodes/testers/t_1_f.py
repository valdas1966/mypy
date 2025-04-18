import pytest
from f_hs.nodes.i_1_f import NodeF


@pytest.fixture
def ex_a() -> NodeF:
    # node.g = 0
    # node.f = 1
    node = NodeF()
    node.h = 1
    return node


@pytest.fixture
def ex_b(ex_a) -> NodeF:
    # node.g = 1
    # node.f = 1
    node = NodeF(parent=ex_a)
    node.h = 0
    return node


def test_key_comparison(ex_a, ex_b):
    assert ex_b < ex_a


def test_repr(ex_a):
    assert repr(ex_a) == '<NodeF: None> G=0, H=1, F=1'
