from f_graph.algos.one_to_one.i_0_base import (AlgoOneToOne, ProblemOneToOne,
                                               TypeQueue, NodePath)
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToOne)
Node = TypeVar('Node', bound=NodePath)


class BFS(AlgoOneToOne[Problem, Node]):
    """
    ============================================================================
     Breadth-First-Search Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 name: str = 'BFS') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToOne.__init__(self,
                              problem=problem,
                              type_queue=TypeQueue.FIFO,
                              name=name)

