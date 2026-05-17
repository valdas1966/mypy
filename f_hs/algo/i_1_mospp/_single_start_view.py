from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class _SingleStartView(Generic[State], ProblemSPP[State]):
    """
    ========================================================================
     ProblemSPP wrapper that exposes exactly one start from a
     multi-start base problem. Delegates everything else.

     Used by AStarRepMOSPP to feed each sub-search a single-
     start problem while keeping the underlying graph /
     successors / edge weights / goals unchanged.

     Mirror of `_SingleGoalView` (in `i_1_omspp/`).
    ========================================================================
    """

    def __init__(self,
                 base: ProblemSPP[State],
                 start: State) -> None:
        """
        ====================================================================
         Init private Attributes. Reuses the base's goals; the
         single-start list overrides base's starts.
        ====================================================================
        """
        ProblemSPP.__init__(self,
                            starts=[start],
                            goals=base.goals,
                            name=base.name)
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
