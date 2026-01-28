from f_search.ds.data.i_0_best_first.main import DataBestFirst
from f_search.ds.state.i_0_base.main import StateBase as State


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
    assert data.path_to(state_a) == path_a
    assert data.path_to(state_b) == path_ab
    assert data.path_to(state_c) == path_abc
