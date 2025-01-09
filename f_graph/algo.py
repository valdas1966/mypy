from f_graph.problem import ProblemGraph, NodeUid
from f_graph.solution import SolutionGraph
from f_core.processes.i_2_io import ProcessIO
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemGraph)
Solution = TypeVar('Solution', bound=SolutionGraph)
Node = TypeVar('Node', bound=NodeUid)


class AlgoGraph(Generic[Problem, Solution, Node],
                ProcessIO[Problem, Solution]):
    """
    ============================================================================
     ABC for Graph-Algorithms in Computer-Science.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 name: str = 'Graph-Algorithm') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProcessIO.__init__(self, _input=problem, name=name)
