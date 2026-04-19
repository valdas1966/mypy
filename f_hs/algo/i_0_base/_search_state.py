from dataclasses import dataclass, field
from typing import Generic, TypeVar

from f_hs.frontier.i_0_base.main import FrontierBase
from f_hs.state.i_0_base.main import StateBase

State = TypeVar('State', bound=StateBase)


@dataclass
class SearchStateSPP(Generic[State]):
    """
    ============================================================================
     Mutable per-search state for AlgoSPP.

     Bundles the five fields that change as the search runs —
     frontier, g-values, parents, closed set, and the goal that
     was reached at termination. Held as a single attribute on
     AlgoSPP (`self._search`) so the algorithm body reads
     `self._search.frontier`, `self._search.g[...]`, etc.

     Why a dataclass and not five separate attributes:
     1. Resumability — `resume()` re-enters the loop without
        clearing this bundle.
     2. Cross-instance inspection — bidirectional search peeks at
        the other side's `closed`/`g` via `algo.search_state`.
     3. Subclass extension — OMSPP adds `goals_reached` and
        `solutions` on a `SearchStateOMSPP(SearchStateSPP)`.

     `goals_set` is intentionally NOT in here: it's derived from
     the (immutable) problem and lives directly on AlgoSPP.
    ============================================================================
    """
    frontier:     FrontierBase[State]
    g:            dict[State, float]              = field(default_factory=dict)
    parent:       dict[State, State | None]       = field(default_factory=dict)
    closed:       set[State]                      = field(default_factory=set)
    goal_reached: State | None                    = None

    def clear(self) -> None:
        """
        ========================================================================
         Reset to a fresh search. Frontier identity is preserved
         (frontier.clear() empties the underlying container);
         g/parent/closed dicts are emptied; goal_reached unset.
        ========================================================================
        """
        self.frontier.clear()
        self.g.clear()
        self.parent.clear()
        self.closed.clear()
        self.goal_reached = None
