import pytest
from f_hs.nodes.i_0_h import NodeH


@pytest.fixture
def ex_a() -> NodeH:
    node = NodeH()
    node.h = 1
    return node


@pytest.fixture
def ex_b() -> NodeH:
    node = NodeH()
    node.h = 2
    return node


def test_key_comparison(ex_a, ex_b):
    assert ex_a < ex_b


def test_repr(ex_a):
    assert repr(ex_a) == '<NodeH: None> H=1'
