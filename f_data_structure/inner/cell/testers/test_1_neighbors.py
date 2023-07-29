from f_data_structure.inner.cell.i_1_neighbors import CellNeighbors


def test_neighbors():
    cell = CellNeighbors(x=1, y=2)
    north = CellNeighbors(x=1, y=3)
    east = CellNeighbors(x=2, y=2)
    south = CellNeighbors(x=1, y=1)
    west = CellNeighbors(x=0, y=2)
    expected = [north, east, south, west]
    assert cell.neighbors() == expected
