from f_ds.grids.u_cell import UCell, Cell


def test_invalidate():
    cell_0 = Cell(0)
    cell_1 = Cell(1)
    assert cell_0 and cell_1
    UCell.invalidate(cell_0, cell_1)
    assert not (cell_0 and cell_1)
