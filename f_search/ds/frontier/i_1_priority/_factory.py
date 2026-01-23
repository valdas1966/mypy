from f_search.ds.frontier.i_1_priority.main import FrontierPriority
from f_search.ds.states.i_0_base.main import StateBase as State
from f_search.ds.priority import PriorityG as Priority


class Factory:
    """
    ============================================================================
     Factory for creating FrontierPriority objects.
    ============================================================================
    """

    @staticmethod
    def abc() -> FrontierPriority[State, Priority]:
        """
        ========================================================================
         Create a new FrontierPriority object with the 'A', 'B', 'C' states and
          mess inserted priorities.
        ========================================================================
        """
        state_a = State.Factory.a()
        state_b = State.Factory.b()
        state_c = State.Factory.c()
        priority_a = Priority(key='A', g=2)
        priority_b = Priority(key='B', g=1)
        priority_c = Priority(key='C', g=3)
        frontier = FrontierPriority[State, Priority]()
        frontier.push(state=state_a, priority=priority_a)
        frontier.push(state=state_b, priority=priority_b)
        frontier.push(state=state_c, priority=priority_c)
        return frontier

    @staticmethod
    def abc_updated() -> FrontierPriority[State, Priority]:
        """
        ========================================================================
         Create a new FrontierPriority object with the 'A', 'B', 'C' states and
          updated priorities.
        ========================================================================
        """
        frontier = FrontierPriority.Factory.abc()
        state = State.Factory.a()
        priority = Priority(key=state.key, g=5)
        frontier.update(state=state, priority=priority)
        return frontier