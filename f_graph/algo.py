from f_graph.problem import ProblemGraph, NodeKey
from f_graph.solution import SolutionGraph
from f_cs.algo import Algo
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemGraph)
Solution = TypeVar('Solution', bound=SolutionGraph)
Node = TypeVar('Node', bound=NodeKey)


class AlgoGraph(Generic[Problem, Solution, Node],
                Algo[Problem, Solution]):
    """
    ============================================================================
     ABC for Graph-Algorithms in Computer-Science.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 verbose: bool = True,
                 name: str = 'Graph-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Algo.__init__(self, problem=problem, verbose=verbose, name=name)
