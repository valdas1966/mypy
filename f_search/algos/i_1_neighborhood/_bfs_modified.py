from f_search.algos.i_1_spp import BFS
from f_search.ds.state import StateBase
from f_search.problems import ProblemSPP as Problem
from typing import Generic, TypeVar

State = TypeVar('State', bound=StateBase)

class BFSModified(Generic[State], BFS[State]):
    """
    ============================================================================
     1. BFS Modified for Neighborhood Problem.
     2. Terminate when the Best.G is greater than the maximum step.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 steps_max: int,
                 name: str = 'BFSModified') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, name=name)
        self._steps_max = steps_max

    def _can_terminate(self) -> bool:
        """
        ========================================================================
         Check if the algorithm can terminate.
        ========================================================================
        """
        data = self._data
        best = data.best
        return data.dict_g[best] > self._steps_max
