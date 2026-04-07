import pytest
from f_hs.problem.i_1_grid import ProblemGrid


@pytest.fixture
def grid_3x3() -> ProblemGrid:
    """
    ========================================================================
     Open 3x3 Grid.
    ========================================================================
    """
    return ProblemGrid.Factory.grid_3x3()


def test_start(grid_3x3: ProblemGrid) -> None:
    """
    ========================================================================
     Test the start state is at (0,0).
    ========================================================================
    """
    assert grid_3x3.start.key.row == 0
    assert grid_3x3.start.key.col == 0


def test_goal(grid_3x3: ProblemGrid) -> None:
    """
    ========================================================================
     Test the goal state is at (2,2).
    ========================================================================
    """
    assert grid_3x3.goal.key.row == 2
    assert grid_3x3.goal.key.col == 2


def test_successors(grid_3x3: ProblemGrid) -> None:
    """
    ========================================================================
     Test successors of corner cell (0,0) are (0,1) and (1,0).
    ========================================================================
    """
    children = grid_3x3.successors(grid_3x3.start)
    keys = {(s.key.row, s.key.col) for s in children}
    assert keys == {(0, 1), (1, 0)}


def test_successors_center(grid_3x3: ProblemGrid) -> None:
    """
    ========================================================================
     Test successors of center cell (1,1) are 4 neighbors.
    ========================================================================
    """
    from f_hs.state.i_1_cell import StateCell
    center = StateCell.Factory.at(row=1, col=1)
    children = grid_3x3.successors(center)
    assert len(children) == 4


def test_successors_obstacle() -> None:
    """
    ========================================================================
     Test that obstacle cell is excluded from successors.
    ========================================================================
    """
    problem = ProblemGrid.Factory.grid_3x3_obstacle()
    from f_hs.state.i_1_cell import StateCell
    cell_01 = StateCell.Factory.at(row=0, col=1)
    children = problem.successors(cell_01)
    keys = {(s.key.row, s.key.col) for s in children}
    assert (1, 1) not in keys
