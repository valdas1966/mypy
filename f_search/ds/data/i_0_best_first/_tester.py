from f_search.ds.data.i_0_best_first.main import DataBestFirst
from f_search.ds.states.i_0_base.main import StateBase as State


def test_path_to() -> None:
    """
    ========================================================================
     Test the DataBestFirst.path_to() method.
    ========================================================================
    """
    data = DataBestFirst.Factory.abc()
    state_a = State.Factory.a()
    state_b = State.Factory.b()
    state_c = State.Factory.c()
    path_a = [state_a]
    path_ab = [state_a, state_b]
    path_abc = [state_a, state_b, state_c]
    assert data.path_to(state_a) == path_a
    assert data.path_to(state_b) == path_ab
    assert data.path_to(state_c) == path_abc
