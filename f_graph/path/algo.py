from f_graph.algo import AlgoGraph
from f_graph.path.problem import ProblemPath
from f_graph.path.solution import SolutionPath
from f_ds.nodes.i_1_heuristic import NodeHeuristic as Node
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Solution = TypeVar('Solution', bound=SolutionPath)


class AlgoPath(Generic[Problem, Solution],
               AlgoGraph[Problem, Solution, Node]):
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
