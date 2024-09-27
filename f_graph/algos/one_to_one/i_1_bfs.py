from f_graph.algos.one_to_one.i_0_base import (AlgoOneToOne, ProblemOneToOne,
                                               NodePath, DataOneToOne)
from f_ds.queues.i_1_fifo import QueueFIFO
from typing import TypeVar

Node = TypeVar('Node', bound=NodePath)
Problem = TypeVar('Problem', bound=ProblemOneToOne)
Data = TypeVar('Data', bound=DataOneToOne)


class BFS(AlgoOneToOne[Node, Problem, Data]):
    """
    ============================================================================
     Breadth-First-Search Algorithm.
    ============================================================================
    """

    def __init__(self, problem: Problem) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToOne.__init__(self,
                              problem=problem,
                              type_data=DataOneToOne,
                              type_queue=QueueFIFO)
