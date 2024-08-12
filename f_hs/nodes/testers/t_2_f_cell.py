from f_hs.nodes.i_1_f_cell import NodeFCell
import pytest


@pytest.fixture
def node_zero() -> NodeFCell:
    node = NodeFCell(name='Zero')
    node.h = 0
    return node


@pytest.fixture
def node_one() -> NodeFCell:
    node = NodeFCell(name='One')
    node.h = 1
    return node


def test_eq(node_zero, node_one):
    assert node_zero == node_one


def test_repr(node_zero, node_one):
    assert repr(node_zero) == '<NodeFCell: Zero(0,0)> G=0, H=0, F=0'
    assert repr(node_one) == '<NodeFCell: One(0,0)> G=0, H=1, F=1'

