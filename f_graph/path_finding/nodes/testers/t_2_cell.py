import pytest
from f_graph.path_finding.nodes.i_2_cell import NodeCell, Cell


@pytest.fixture
def ex_00() -> NodeCell:
    return NodeCell(name='Zero')


@pytest.fixture
def ex_11() -> NodeCell:
    return NodeCell(name='One', cell=Cell(1))


@pytest.fixture
def ex_00_other() -> NodeCell:
    return NodeCell()


def test_key_comparison(ex_00, ex_11):
    assert ex_00 < ex_11


def test_str(ex_00, ex_11):
    assert str(ex_00) == 'Zero(0,0)'
    assert str(ex_11) == 'One(1,1)'


def test_eq(ex_00, ex_00_other):
    assert ex_00 == ex_00_other


def test_hash():
    # Test the Hash by Cell (not by Name)
    a = NodeCell(name='Node', cell=Cell(0))
    b = NodeCell(name='Node', cell=Cell(1))
    c = NodeCell(cell=Cell(1))
    assert {a, b} == {a, b}
    assert {b, c} == {b}
