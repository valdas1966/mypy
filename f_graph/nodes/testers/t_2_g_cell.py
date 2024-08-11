from f_graph.nodes.i_2_g_cell import NodeGCell, Cell
import pytest


@pytest.fixture
def node_zero() -> NodeGCell:
    return NodeGCell(name='Zero')


@pytest.fixture
def node_one() -> NodeGCell:
    return NodeGCell(name='One', cell=Cell(1, 1))


def test_key_comparison(node_zero, node_one) -> None:
    assert node_zero < node_one


def test_str(node_zero, node_one) -> None:
    assert str(node_zero) == 'Zero(0,0)'
    assert str(node_one) == 'One(1,1)'


def test_hash(node_zero, node_one) -> None:
    assert len({node_zero, node_one}) == 2
