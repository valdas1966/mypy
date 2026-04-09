from f_hs.problem.i_1_grid import ProblemGrid
from f_hs.state.i_1_cell import StateCell


def test_start() -> None:
    """
    ========================================================================
     Test the start state is at (0,0).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3()
    assert problem.start.rc == (0, 0)


def test_goal() -> None:
    """
    ========================================================================
     Test the goal state is at (2,2).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3()
    assert problem.goal.rc == (2, 2)


def test_successors() -> None:
    """
    ========================================================================
     Test successors of corner cell (0,0) are (0,1) and (1,0).
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3()
    children = problem.successors(problem.start)
    keys = {s.rc for s in children}
    assert keys == {(0, 1), (1, 0)}


def test_successors_center() -> None:
    """
    ========================================================================
     Test successors of center cell (1,1) are 4 neighbors.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3()
    center = StateCell.Factory.at(row=1, col=1)
    children = problem.successors(center)
    assert len(children) == 4


def test_successors_obstacle() -> None:
    """
    ========================================================================
     Test that obstacle cell is excluded from successors.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3_obstacle()
    cell_01 = StateCell.Factory.at(row=0, col=1)
    children = problem.successors(cell_01)
    assert len(children) == 2
