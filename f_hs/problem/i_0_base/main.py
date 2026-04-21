from f_cs.problem import ProblemAlgo
from f_hs.state import StateBase
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)


class ProblemSPP(ProblemAlgo, Generic[State]):
    """
    ============================================================================
     Shortest-Path-Problem (covers OO, OM, MO, and MM variants).
    ============================================================================
    """

    def __init__(self,
                 starts: list[State],
                 goals: list[State],
                 name: str = 'ProblemSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemAlgo.__init__(self, name=name)
        self._starts: list[State] = starts
        self._goals: list[State] = goals

    @property
    def starts(self) -> list[State]:
        """
        ========================================================================
         Return the list of Start States.
        ========================================================================
        """
        return self._starts

    @property
    def goals(self) -> list[State]:
        """
        ========================================================================
         Return the list of Goal States.
        ========================================================================
        """
        return self._goals

    @property
    def start(self) -> State:
        """
        ========================================================================
         Return the first Start State (convenience for single-start).
        ========================================================================
        """
        return self._starts[0]

    @property
    def goal(self) -> State:
        """
        ========================================================================
         Return the first Goal State (convenience for single-goal).
        ========================================================================
        """
        return self._goals[0]

    def w(self, parent: State, child: State) -> int:
        """
        ========================================================================
         Return the Edge Cost from Parent to Child.

         Integer-weight assumption: the framework treats edge
         costs as `int` in its hot path. Heuristics should also
         return `int`. Fractional weights would require a
         separate weighted variant (not shipped). `float('inf')`
         remains the sentinel for unreachable states in Solution
         cost and internal `g` storage — localised to that one
         case.
        ========================================================================
        """
        return 1

    def successors(self, state: State) -> list[State]:
        """
        ========================================================================
         Return the Successors of the given State.
        ========================================================================
        """
        raise NotImplementedError

    @property
    def key(self) -> tuple:
        """
        ========================================================================
         Return the Problem's Key for Equality.
        ========================================================================
        """
        return (tuple(self._starts), tuple(self._goals))

    def __hash__(self) -> int:
        """
        ========================================================================
         Return the Hash of the Problem.
        ========================================================================
        """
        return hash(self.key)
