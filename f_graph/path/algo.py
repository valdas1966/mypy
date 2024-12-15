from f_graph.algo import AlgoGraph
from f_graph.path.data.problem import ProblemPath
from f_graph.path.data.solution import SolutionPath
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Solution = TypeVar('Solution', bound=SolutionPath)


class AlgoPath(Generic[Problem, Solution], AlgoGraph[Problem, Solution]):
    """
    ============================================================================
     ABC for Path-Finding Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 name: str = 'Path-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoGraph.__init__(self, problem=problem, name=name)


