from f_ds.grids.cell.i_1_map import CellMap as Cell
from f_search.ds.states.i_0_base.main import StateBase


class Factory:
    """
    ============================================================================
     Factory for creating States.
    ============================================================================
    """

    @staticmethod
    def a() -> StateBase[str]:
        """
        ========================================================================
         Return a new StateBase with the key 'A'.
        ========================================================================
        """
        return StateBase[str](key='A', name='A')

    @staticmethod
    def b() -> StateBase[str]:
        """
        ========================================================================
         Return a new StateBase with the key 'B'.
        ========================================================================
        """
        return StateBase[str](key='B', name='B')
