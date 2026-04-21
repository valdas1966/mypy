from f_hs.problem.i_0_base.main import ProblemSPP
from f_hs.state.i_0_base.main import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class _SingleGoalView(Generic[State], ProblemSPP[State]):
    """
    ========================================================================
     ProblemSPP wrapper that exposes exactly one goal from a
     multi-goal base problem. Delegates everything else.

     Used by KAStarInc to feed each sub-search a single-goal
     problem while keeping the underlying graph / successors /
     edge weights unchanged.
    ========================================================================
    """

    def __init__(self,
                 base: ProblemSPP[State],
                 goal: State) -> None:
        """
        ====================================================================
         Init private Attributes. Reuses the base's starts; the
         single-goal list overrides base's goals.
        ====================================================================
        """
        ProblemSPP.__init__(self,
                            starts=base.starts,
                            goals=[goal],
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
