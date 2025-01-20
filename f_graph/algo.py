from f_graph.problem import ProblemGraph, NodeUid
from f_graph.solution import SolutionGraph, StatsAlgo
from f_cs.algo import Algo
from typing import Generic, TypeVar

Problem = TypeVar('Problem', bound=ProblemGraph)
Solution = TypeVar('Solution', bound=SolutionGraph)
Stats = TypeVar('Stats', bound=StatsAlgo)
Node = TypeVar('Node', bound=NodeUid)


class AlgoGraph(Generic[Problem, Solution, Stats, Node],
                Algo[Problem, Solution[Stats]]):
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
        Algo.__init__(self, _input=problem, name=name)  
