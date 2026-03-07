import pickle
from f_search.problems.i_0_base.main import ProblemSearch
from f_search.ds.state import StateBase


def test_successors() -> None:
    """
    ========================================================================
     Test the successors() method.
    ========================================================================
    """
    problem = ProblemSearch.Factory.four_with_obstacles()
    cell_00 = problem.grid[0][0]
    cell_01 = problem.grid[0][1]
    cell_10 = problem.grid[1][0]
    state_00 = StateBase(key=cell_00)
    state_01 = StateBase(key=cell_01)
    state_10 = StateBase(key=cell_10)
    successors = problem.successors(state=state_00)
    successors_true = [state_01, state_10]
    assert successors == successors_true


def test_pickle_excludes_grid() -> None:
    """
    ========================================================================
     Test that pickle excludes the heavy Grid and load_grid restores it.
    ========================================================================
    """
    problem = ProblemSearch.Factory.four_with_obstacles()
    grid = problem.grid
    # Pickle and unpickle
    data = pickle.dumps(problem)
    loaded = pickle.loads(data)
    # Grid is None after unpickle
    assert loaded._grid is None
    # name_grid survives pickle
    assert loaded.name_grid == 'Grid4x4Obstacles'
    # Restore grid
    grids = {grid.name: grid}
    loaded.load_grid(grids=grids)
    assert loaded.grid == grid


def test_to_analytics() -> None:
    """
    ========================================================================
     Test the to_analytics() method.
    ========================================================================
    """
    problem = ProblemSearch.Factory.four_with_obstacles()
    d = problem.to_analytics()
    assert d['rows'] == 4
    assert d['cols'] == 4
    assert d['cells'] == 14
    assert d['map'] == 'Grid4x4Obstacles'
    assert 'domain' in d
