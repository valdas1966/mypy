from f_search.ds.path.main import Path
from f_search.ds.state.i_0_base._factory import StateBase


class Factory:
    """
    ============================================================================
     Factory for creating Paths.
    ============================================================================
    """

    @staticmethod
    def ab() -> Path:
        """
        ========================================================================
         Return a new Path with the state A and B.
        ========================================================================
        """
        a = StateBase.Factory.a()
        b = StateBase.Factory.b()
        states = [a, b]
        return Path(states=states)
