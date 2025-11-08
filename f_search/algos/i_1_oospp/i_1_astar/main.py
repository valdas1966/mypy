from f_search.algos import AlgoOOSPP, ProblemOOSPP, SolutionOOSPP
from f_ds.queues.i_1_priority import QueuePriority
from f_search.state import State


class AStar(AlgoOOSPP):
    """
    ============================================================================
     A* Algorithm for One-to-One Shortest-Path-Problem.
    ============================================================================
    """
    def __init__(self,
                 problem: ProblemOOSPP,
                 verbose: bool = True,
                 name: str = 'AStar') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOOSPP.__init__(self, problem=problem, verbose=verbose, name=name)
        self._generated: QueuePriority[State] = QueuePriority()

    def run(self) -> SolutionOOSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        pass