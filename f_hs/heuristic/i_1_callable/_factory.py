from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ========================================================================
     Factory for HCallable test instances.
    ========================================================================
    """

    @staticmethod
    def zero() -> HCallable[StateBase[str]]:
        """
        ====================================================================
         h(s) = 0 — the trivial admissible heuristic.
        ====================================================================
        """
        return HCallable[StateBase[str]](fn=lambda s: 0.0)

    @staticmethod
    def graph_abc() -> HCallable[StateBase[str]]:
        """
        ====================================================================
         Admissible h for graph_abc: h(A)=2, h(B)=1, h(C)=0.
        ====================================================================
        """
        h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
        return HCallable[StateBase[str]](
            fn=lambda s: h_map.get(s.key, 0.0))
