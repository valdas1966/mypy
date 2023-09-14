from f_heuristic_search.alias.cell import Cell
from f_heuristic_search.nodes.node_1_cell import NodeCell


def test_name():
    cell = Cell(row=1, col=1, name='cell')
    node = NodeCell(cell=cell, name='node')
    assert node.name == 'node'


def test_eq():
    cell_1 = Cell(1, 1)
    cell_2 = Cell(1, 1)
    cell_3 = Cell(2, 2)
    node_1 = NodeCell(cell=cell_1)
    node_2 = NodeCell(cell=cell_2)
    node_3 = NodeCell(cell=cell_3)
    assert (node_1 == node_2)
    assert not (node_1 == node_3)
