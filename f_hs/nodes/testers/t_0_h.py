import pytest
from f_hs.nodes.mixins.has_h import NodeH


@pytest.fixture
def ex_a() -> NodeH:
    node = NodeH()
    node.h = 5
    return node


@pytest.fixture
def ex_b(ex_a) -> NodeH:
    node = NodeH()
    node.h = 10
    return node


def test_key_comparison(ex_a, ex_b):
    assert ex_a < ex_b


def test_repr(ex_a):
    assert repr(ex_a) == '<NodeH: None> H=5'
