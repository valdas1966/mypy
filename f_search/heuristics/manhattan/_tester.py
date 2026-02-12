from f_search.heuristics.manhattan import HeuristicsManhattan
from f_search.ds.state import StateCell as State


def test_manhattan_distance() -> None:
    """
    ========================================================================
     Test that manhattan distance heuristic calculates correct distances.
    ========================================================================
    """
    heuristics = HeuristicsManhattan.Factory.cell_01()
    state_01 = State.Factory.cell_01()
    state_10 = State.Factory.cell_10()
    assert heuristics(state=state_01) == 0
    assert heuristics(state=state_10) == 2
