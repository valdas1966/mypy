from f_ds.grids.connectivity.i_1_04.main import Connectivity_4
from f_ds.geometry.point2d import Point2D


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
    a = Point2D(row=0, col=0)
    b = Point2D(row=0, col=1)
    assert connectivity.cost(a=a, b=b) == 1


def test_distance() -> None:
    """
    ========================================================================
     Test the Manhattan distance (admissible 4-conn heuristic).
    ========================================================================
    """
    connectivity = Connectivity_4()
    a = Point2D(row=0, col=0)
    b = Point2D(row=2, col=3)
    assert connectivity.distance(a=a, b=b) == 5
