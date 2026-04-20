from f_hs.heuristic.i_0_base.main import HBase
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class HBounded(Generic[State], HBase[State]):
    """
    ============================================================================
     Heuristic Source wrapping a base HBase with a frozen dict
     of admissible lower bounds.

     Semantics:
       - On a bounded hit:  h := max(base(state), bounds[state]).
       - On a bounded miss: h := base(state).
       - is_perfect(s)  — False always (inherited). Bounds are
                          admissible, NOT perfect — a bound can
                          be looser than h*, so early-termination
                          must not fire.
       - suffix_next(s) — None always (inherited). Bounds carry
                          no path information.

     **Admissibility contract** — bound[s] <= h*(s) for every
     bounded state. Caller's responsibility; not enforced at
     runtime (no cheap way to verify against h* in general).
     Violating this silently breaks A*'s optimality.

     Static bounds: the constructor takes a defensive shallow
     copy of the dict; no mutation API (mirrors HCached's
     2026-04-20 static-cache decision).

     Zero AStar changes: AStar._priority reads self._h(state),
     which auto-routes through the max-combine. cache_rank stays
     1 (is_perfect=False), so tie-break ordering is unchanged.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 base: HBase[State],
                 bounds: dict[State, float]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._base = base
        self._bounds: dict[State, float] = dict(bounds)

    @property
    def bounds(self) -> dict[State, float]:
        """
        ========================================================================
         Read-only view of the bounds (shallow copy).
        ========================================================================
        """
        return dict(self._bounds)

    def __call__(self, state: State) -> float:
        """
        ========================================================================
         Return max(base(state), bounds[state]) on a bounded hit;
         delegate to base on a miss.
        ========================================================================
        """
        b = self._bounds.get(state)
        if b is None:
            return self._base(state)
        return max(self._base(state), b)

    def is_bounded(self, state: State) -> bool:
        """
        ========================================================================
         True iff bounds[state] exists AND is strictly greater
         than base(state). Semantics: "the bound tightened h
         beyond what the base provides." Misses and ties both
         return False — ties add no new info beyond base.

         Chosen for parallel semantics with HCached.is_perfect:
         each flag's presence unambiguously means "the
         specialized source determined h." Avoids misleading
         records where a weaker-than-base bound would otherwise
         be flagged despite having no effect.
        ========================================================================
        """
        b = self._bounds.get(state)
        if b is None:
            return False
        return b > self._base(state)

    def add_bound(self, state: State, value: float) -> bool:
        """
        ========================================================================
         Insert `value` as a bound on `state` iff it STRICTLY
         tightens the current effective h, i.e.,
             value > self(state)     # max(base, existing_bound)
         On a strict win, overwrite (or insert) and return True.
         On a tie or weaker, no-op and return False.

         **Pre-search propagation only.** This is the one narrow
         relaxation of the static-bounds invariant: the ctor
         still takes a defensive copy at __init__, and no other
         public mutation exists. `add_bound` is consumed
         exclusively by `AStar.propagate_pathmax` (Phase 2b),
         which runs as a setup step before the search loop —
         during the search, bounds remain effectively static.

         Admissibility: caller's responsibility. Pathmax's
         `h(s) - w(s, n)` insertions are admissible by the
         inequality `h*(n) >= h*(s) - w(s, n)`.
        ========================================================================
        """
        if value > self(state):
            self._bounds[state] = value
            return True
        return False
