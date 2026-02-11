from f_search.problems.i_0_base.main import ProblemSearch
from f_search.ds.state import StateBase


def test_successors() -> None:
    """
    ========================================================================
     Test the successors() method.
    ========================================================================
    """
    problem = ProblemSearch.Factory.grid_3x3()
    cell_00 = problem.grid[0][0]
    cell_01 = problem.grid[0][1]
    cell_10 = problem.grid[1][0]
    state_00 = StateBase(key=cell_00)
    state_01 = StateBase(key=cell_01)
    state_10 = StateBase(key=cell_10)
    successors = problem.successors(state=state_00)
    successors_true = [state_01, state_10]
    assert successors == successors_true
