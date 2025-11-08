from f_search.problems.mixins.has_grid.main import HasGrid
from f_search.state import State


def test_successors() -> None:
    """
    ========================================================================
     Test the successors() method.
    ========================================================================
    """
    has_grid = HasGrid.Factory.grid_3x3()
    cell_00 = has_grid.grid[0][0]
    cell_01 = has_grid.grid[0][1]
    cell_10 = has_grid.grid[1][0]
    state_00 = State(key=cell_00)
    state_01 = State(key=cell_01)
    state_10 = State(key=cell_10)
    successors = has_grid.successors(state=state_00)
    successors_true = [state_01, state_10]
    assert successors == successors_true
