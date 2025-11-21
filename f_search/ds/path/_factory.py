from f_search.ds.path.main import Path
from f_search.ds.states.i_0_base._factory import StateBase


class Factory:
    """
    ============================================================================
     Factory for creating Paths.
    ============================================================================
    """

    @staticmethod
    def diagonal() -> Path:
        """
        ========================================================================
         Return a new Path with the states (0, 0), (1, 1), (2, 2).
        ========================================================================
        """
        zero = StateBase.Factory.zero()
        one = StateBase.Factory.one()
        two = StateBase.Factory.two()
        states = [zero, one, two]
        return Path(states=states)
