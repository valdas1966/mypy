from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class _FlippedView(Generic[State], ProblemSPP[State]):
    """
    ========================================================================
     ProblemSPP view that SWAPS `starts` and `goals` of a base
     problem (the One-to-Many / Many-to-One axis flip).

     Returned by `ProblemSPP.flipped()`. `successors()` and
     `w()` delegate to the base UNCHANGED, so the same
     `(parent, child)` edges are walked. On an UNDIRECTED graph
     the flipped problem is the genuine transpose
     (`dist(s, t) == dist(t, s)`); on a directed graph it
     relabels endpoints WITHOUT reversing edges, and the caller
     owns that precondition.
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
