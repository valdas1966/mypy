from f_search.ds.frontier.i_1_priority.main import FrontierPriority
from f_search.ds.state import StateBase, StateCell
from f_search.ds.priority import PriorityG
from f_search.ds.priority import PriorityGH


class Factory:
    """
    ============================================================================
     Factory for creating FrontierPriority objects.
    ============================================================================
    """

    @staticmethod
    def abc() -> FrontierPriority[StateBase, PriorityG]:
        """
        ========================================================================
         Create a new FrontierPriority object with the 'A', 'B', 'C' state and
          mess inserted priorities.
        ========================================================================
        """
        state_a = StateBase.Factory.a()
        state_b = StateBase.Factory.b()
        state_c = StateBase.Factory.c()
        priority_a = PriorityG(key='A', g=2)
        priority_b = PriorityG(key='B', g=1)
        priority_c = PriorityG(key='C', g=3)
        frontier = FrontierPriority[StateBase, PriorityG]()
        frontier.push(state=state_a, priority=priority_a)
        frontier.push(state=state_b, priority=priority_b)
        frontier.push(state=state_c, priority=priority_c)
        return frontier

    @staticmethod
    def abc_updated() -> FrontierPriority[StateBase, PriorityG]:
        """
        ========================================================================
         Create a new FrontierPriority object with the 'A', 'B', 'C' state and
          updated priorities.
        ========================================================================
        """
        frontier = FrontierPriority.Factory.abc()
        state = StateBase.Factory.a()
        priority = PriorityG(key=state.key, g=5)
        frontier.update(state=state, priority=priority)
        return frontier

    @staticmethod
    def cells_01_10() -> FrontierPriority[StateCell, PriorityGH]:
        """
        ========================================================================
         Create a new FrontierPriority object with the cells (0, 1) and (1, 0).
        ========================================================================
        """
        state_01 = StateCell.Factory.cell_01()
        state_10 = StateCell.Factory.cell_10()
        priority_01 = PriorityGH(key=state_01.key, g=1, h=2)
        priority_10 = PriorityGH(key=state_10.key, g=1, h=4)
        frontier = FrontierPriority[StateCell, PriorityGH]()
        frontier.push(state=state_01, priority=priority_01)
        frontier.push(state=state_10, priority=priority_10)
        return frontier
    