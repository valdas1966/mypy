from f_hs.nodes.i_0_g import NodeG
import pytest


@pytest.fixture
def node_a() -> NodeG:
    return NodeG(name='A')


@pytest.fixture
def node_b(node_a) -> NodeG:
    return NodeG(name='B', parent=node_a)


@pytest.fixture
def node_c(node_b) -> NodeG:
    return NodeG(name='C', parent=node_b)


def test_g(node_a, node_b, node_c) -> None:
    assert node_a.g == 0
    assert node_b.g == 1
    assert node_c.g == 2


def test_set_parent(node_a, node_c) -> None:
    node_c.parent = node_a
    assert node_c.g == 1


def test_is_better_parent(node_a, node_b, node_c) -> None:
    assert node_a.is_better_parent(node_b)
    assert not node_b.is_better_parent(node_c)
    assert node_c.is_better_parent(node_a)


def test_key_comparison(node_a, node_b) -> None:
    assert not node_a < node_a
    assert node_b < node_a


def test_repr(node_a) -> None:
    assert repr(node_a) == '<NodeG: A> G=0'
