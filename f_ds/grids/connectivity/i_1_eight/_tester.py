from f_ds.grids.connectivity.i_1_eight.main import Connectivity8
from f_ds.grids.cell import CellMap


def test_offsets() -> None:
    """
    ========================================================================
     Test there are 8 offsets (cardinals + diagonals).
    ========================================================================
    """
    connectivity = Connectivity8()
    assert len(connectivity.offsets) == 8


def test_cost_cardinal() -> None:
    """
    ========================================================================
     Test a cardinal move costs COST_CARDINAL.
    ========================================================================
    """
    connectivity = Connectivity8()
    a = CellMap(row=0, col=0)
    b = CellMap(row=0, col=1)
    assert connectivity.cost(a=a, b=b) == 10_000


def test_cost_diagonal() -> None:
    """
    ========================================================================
     Test a diagonal move costs COST_DIAGONAL.
    ========================================================================
    """
    connectivity = Connectivity8()
    a = CellMap(row=0, col=0)
    b = CellMap(row=1, col=1)
    assert connectivity.cost(a=a, b=b) == 14_142


def test_heuristic() -> None:
    """
    ========================================================================
     Test the scaled-integer octile heuristic
     (d_min=2, d_max=3 -> 14142*2 + 10000*1).
    ========================================================================
    """
    connectivity = Connectivity8()
    a = CellMap(row=0, col=0)
    b = CellMap(row=2, col=3)
    assert connectivity.heuristic(a=a, b=b) == 38_284


def test_is_legal_move_diagonal_free() -> None:
    """
    ========================================================================
     Test a diagonal is legal when both flanks are free.
    ========================================================================
    """
    connectivity = Connectivity8()
    a = CellMap(row=1, col=0)
    b = CellMap(row=0, col=1)
    is_free = lambda row, col: True
    assert connectivity.is_legal_move(a=a, b=b, is_free=is_free) is True


def test_is_legal_move_corner_cut() -> None:
    """
    ========================================================================
     Test a diagonal is illegal when a flank cell is blocked
     (strict no-corner-cutting).
    ========================================================================
    """
    connectivity = Connectivity8()
    a = CellMap(row=1, col=0)
    b = CellMap(row=0, col=1)
    # (0, 0) is blocked -> the diagonal clips its corner
    blocked = {(0, 0)}
    is_free = lambda row, col: (row, col) not in blocked
    assert connectivity.is_legal_move(a=a, b=b, is_free=is_free) is False
