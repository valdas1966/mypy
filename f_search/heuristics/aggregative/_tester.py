from f_search.heuristics.aggregative import HeuristicsAggregative
from f_search.ds.state import StateCell as State

def test_01_10() -> None:
    """
    ========================================================================
     Test the Aggregative Heuristic for cells 01 and 10.
    ========================================================================
    """
    heuristics = HeuristicsAggregative.Factory.cell_01_10()
    state_00 = State.Factory.zero()
    assert heuristics(state=state_00) == 1
