from f_ds.grids.connectivity.i_1_04.main import Connectivity_4
from f_ds.grids.cell import CellMap


def test_offsets() -> None:
    """
    ========================================================================
     Test the 4 cardinal offsets (N, E, S, W).
    ========================================================================
    """
    connectivity = Connectivity_4()
    assert connectivity.offsets == ((-1, 0), (0, 1), (1, 0), (0, -1))


def test_cost() -> None:
    """
    ========================================================================
     Test the uniform edge cost of 1.
    ========================================================================
    """
    connectivity = Connectivity_4()
    a = CellMap(row=0, col=0)
    b = CellMap(row=0, col=1)
    assert connectivity.cost(a=a, b=b) == 1


def test_heuristic() -> None:
    """
    ========================================================================
     Test the Manhattan heuristic.
    ========================================================================
    """
    connectivity = Connectivity_4()
    a = CellMap(row=0, col=0)
    b = CellMap(row=2, col=3)
    assert connectivity.heuristic(a=a, b=b) == 5
