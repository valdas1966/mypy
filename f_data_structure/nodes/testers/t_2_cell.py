from f_data_structure.nodes.i_2_cell import NodeCell
from f_data_structure.f_grid.cell import Cell


def test_str():
    a = NodeCell()
    assert str(a) == '(0,0)'
    b = NodeCell(name='B')
    assert str(b) == 'B(0,0)'


def test_sort():
    # Test that the Sort is by Cell and not by Node
    a = NodeCell(name='A')
    b = NodeCell(name='B')
    assert a == b
    c = NodeCell(name='A', cell=Cell(1, 1))
    assert c > a
