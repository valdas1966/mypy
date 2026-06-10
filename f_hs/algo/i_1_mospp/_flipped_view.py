from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class _FlippedView(Generic[State], ProblemSPP[State]):
    """
    ========================================================================
     ProblemSPP wrapper that SWAPS `starts` and `goals` from a
     base MOSPP problem to expose it as an OMSPP problem (the
     base's single goal becomes the OMSPP shared start; the
     base's k starts become the OMSPP k goals).

     Used by `BFSFlipMOSPP` and `DijkstraFlipMOSPP` to delegate to
     the OMSPP single-pass orchestrators (`KBFS`, `KDijkstra`).
     `successors()` and `w()` delegate to the base unchanged —
     so the same `(parent, child)` edges are walked. On an
     UNDIRECTED graph this is correct (`dist(t, s) == dist(s,
     t)`); on a directed graph it computes `dist(t, s)` instead
     of `dist(s, t)` and is WRONG. The delegating algos
     document this precondition.

     Sibling of `_SingleStartView` (which exposes one start out
     of many).
    ========================================================================
    """

    def __init__(self, base: ProblemSPP[State]) -> None:
        """
        ====================================================================
         Init private Attributes. The base's goals become the
         flipped view's starts; the base's starts become the
         flipped view's goals.
        ====================================================================
        """
        ProblemSPP.__init__(self,
                            starts=list(base.goals),
                            goals=list(base.starts),
                            name=f'{base.name}[flipped]')
        self._base = base

    def successors(self, state: State) -> list[State]:
        """
        ====================================================================
         Delegate to the base problem.
        ====================================================================
        """
        return self._base.successors(state)

    def w(self, parent: State, child: State) -> int:
        """
        ====================================================================
         Delegate to the base problem's edge cost.
        ====================================================================
        """
        return self._base.w(parent=parent, child=child)
