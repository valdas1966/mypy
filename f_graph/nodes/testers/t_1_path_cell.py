import pytest
from f_graph.nodes.i_1_path_cell import NodePathCell, Cell


@pytest.fixture
def ex_00() -> NodePathCell:
    return NodePathCell(name='Zero')


@pytest.fixture
def ex_11() -> NodePathCell:
    return NodePathCell(name='One', cell=Cell(1))


def test_key_comparison(ex_00, ex_11):
    assert ex_00 < ex_11


def test_str(ex_00, ex_11):
    assert str(ex_00) == 'Zero(0,0)'
    assert str(ex_11) == 'One(1,1)'


def test_hash():
    # Test the Hash by Cell (not by Name)
    a = NodePathCell(name='Node', cell=Cell(0))
    b = NodePathCell(name='Node', cell=Cell(1))
    c = NodePathCell(cell=Cell(1))
    assert {a, b} == {a, b}
    assert {b, c} == {b}
