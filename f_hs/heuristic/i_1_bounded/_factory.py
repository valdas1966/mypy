from f_hs.heuristic.i_1_bounded.main import HBounded
from f_hs.heuristic.i_1_callable.main import HCallable
from f_hs.state.i_0_base.main import StateBase


class Factory:
    """
    ========================================================================
     Factory for HBounded test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc_tight() -> HBounded[StateBase[str]]:
        """
        ====================================================================
         HBounded over a weak base (h=0). Bound A with 2.0 and B
         with 1.0 — both equal h* on the linear graph A->B->C.
         On hits, bound wins (max(0, 2) = 2). On miss (C), base
         returns 0 (== h*).
        ====================================================================
        """
        a, b = (StateBase[str](key=k) for k in 'AB')
        bounds = {a: 2.0, b: 1.0}
        return HBounded(base=HCallable(fn=lambda s: 0.0),
                        bounds=bounds)

    @staticmethod
    def graph_abc_weaker_than_base() -> HBounded[StateBase[str]]:
        """
        ====================================================================
         HBounded whose bounds are WEAKER than the base callable:
         base(A)=2, bound[A]=1. max(2, 1) = 2 — base wins on hit.
         Pins the max-combine semantics (never degrades base).
        ====================================================================
        """
        a = StateBase[str](key='A')
        h_map = {'A': 2.0, 'B': 1.0, 'C': 0.0}
        return HBounded(
            base=HCallable(fn=lambda s: h_map.get(s.key, 0.0)),
            bounds={a: 1.0},
        )
