from f_data_structure.f_grid.cell_traversable import CellTraversable


def test_traversable():
    cell = CellTraversable(1)
    assert cell.is_traversable
    cell.is_traversable = False
    assert not cell.is_traversable
