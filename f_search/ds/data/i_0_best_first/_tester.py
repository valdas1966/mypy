from f_search.ds.data.i_0_best_first.main import DataBestFirst
from f_search.ds.state.i_0_base.main import StateBase as State
from f_ds.grids.cell.i_1_map import CellMap as Cell


def test_path_to() -> None:
    """
    ========================================================================
     Test the DataBestFirst.path_to() method.
    ========================================================================
    """
    data = DataBestFirst.Factory.empty()
    state_a = State.Factory.a()
    state_b = State.Factory.b()
    state_c = State.Factory.c()
    data.frontier.push(state_a)
    data.frontier.push(state_b)
    data.frontier.push(state_c)
    data.dict_parent[state_a] = None
    data.dict_parent[state_b] = state_a
    data.dict_parent[state_c] = state_b
    path_a = [state_a]
    path_ab = [state_a, state_b]
    path_abc = [state_a, state_b, state_c]
    assert data.path_to(state_a).key_comparison() == path_a
    assert data.path_to(state_b).key_comparison() == path_ab
    assert data.path_to(state_c).key_comparison() == path_abc


def test_cell_00() -> None: 
    """
    ========================================================================
     Test the DataBestFirst.cell_00() method.
    ========================================================================
    """
    data = DataBestFirst.Factory.cell_00()
    assert len(data.frontier) == 2
    assert len(data.explored) == 1
