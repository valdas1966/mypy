from f_data_structure.inner.cell.i_1_neighbors import CellNeighbors


def test_neighbors():
    cell = CellNeighbors(x=1, y=2)
    north = CellNeighbors(x=1, y=3)
    east = CellNeighbors(x=2, y=2)
    south = CellNeighbors(x=1, y=1)
    west = CellNeighbors(x=0, y=2)
    expected = [north, east, south, west]
    assert cell.neighbors() == expected


def test_neighbor_north():
    cell = CellNeighbors(x=1, y=2)
    expected = CellNeighbors(x=1, y=3)
    assert cell.neighbor_north() == expected


def test_neighbor_south():
    cell = CellNeighbors(x=1, y=2)
    expected = CellNeighbors(x=1, y=1)
    assert cell.neighbor_south() == expected


def test_neighbor_west():
    cell = CellNeighbors(x=1, y=2)
    expected = CellNeighbors(x=0, y=2)
    assert cell.neighbor_west() == expected


def test_neighbor_east():
    cell = CellNeighbors(x=1, y=2)
    expected = CellNeighbors(x=2, y=2)
    assert cell.neighbor_east() == expected
