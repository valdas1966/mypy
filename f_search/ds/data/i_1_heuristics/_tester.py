from f_search.ds.data.i_1_heuristics.main import DataHeuristics
from f_search.ds.state.i_1_cell.main import StateCell as State


def test_data_state() -> None:
    """
    ========================================================================
     Test the data_state() method.
    ========================================================================
    """
    data = DataHeuristics.Factory.cell_00()
    state_00 = State.Factory.zero()
    state_01 = State.Factory.cell_01()
    assert data.data_state(state_00) == {'key': state_00.key,
                                         'f': 3,
                                         'g': 0,
                                         'h': 3}
    assert data.data_state(state_01) == {'key': state_01.key,
                                         'f': 3,
                                         'g': 1,
                                         'h': 2}
