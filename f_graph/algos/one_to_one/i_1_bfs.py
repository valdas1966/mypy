from f_graph.algos.one_to_one.i_0_base import (AlgoOneToOne, ProblemOneToOne,
                                               TerminationCache, NodePath)
from f_ds.queues.i_1_fifo import QueueFIFO
from typing import TypeVar, Type

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
                 cache: set[Node] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToOne.__init__(self,
                              problem=problem,
                              type_queue=QueueFIFO,
                              cache=cache)
