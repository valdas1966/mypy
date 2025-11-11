from f_search.ds.path.main import Path
from f_search.ds.state._factory import State


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
        zero = State.Factory.zero()
        one = State.Factory.one()
        two = State.Factory.two()
        states = [zero, one, two]
        return Path(states=states)
