from f_hs.nodes.i_3_f_cell import NodeFCell
from f_ds.grids.cell import Cell


def test_from_cell():
    cell = Cell(2, 3)
    node = NodeFCell(cell=cell)
    assert node.cell.row, node.cell.col == (2, 3)
