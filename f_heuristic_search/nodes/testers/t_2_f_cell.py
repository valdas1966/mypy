from f_heuristic_search.nodes.i_3_f_cell import NodeFCell
from f_data_structure.f_grid.cell import Cell


def test_from_cell():
    cell = Cell(2, 3)
    node = NodeFCell(cell)
    assert node.row, node.col == (2, 3)
