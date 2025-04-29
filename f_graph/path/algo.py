from f_cs.mixins.has_eager import HasEager
from f_graph.algo import AlgoGraph
from f_graph.path.problem import ProblemPath
from f_graph.path.solution import SolutionPath
from f_graph.path.node import NodePath as Node
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemPath)
Solution = TypeVar('Solution', bound=SolutionPath)


class AlgoPath(Generic[Problem, Solution],
               AlgoGraph[Problem, Solution, Node],
               HasEager):
    """
    ============================================================================
     ABC for Path-Finding Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 is_eager: bool = False,
                 verbose: bool = False,
                 name: str = 'Path-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasEager.__init__(self, is_eager=is_eager)
        AlgoGraph.__init__(self, problem=problem, verbose=verbose, name=name)
