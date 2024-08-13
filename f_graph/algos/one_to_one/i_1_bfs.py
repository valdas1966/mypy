from f_graph.algos.one_to_one.i_0_base import (AlgoOneToOne, ProblemOneToOne,
                                               NodePath)
from f_ds.queues.i_1_fifo import QueueFIFO
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class BFS(Generic[Node], AlgoOneToOne[Node]):
    """
    ============================================================================
     Breadth-First-Search Algorithm.
    ============================================================================
    """

    def __init__(self, problem: ProblemOneToOne) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOneToOne.__init__(self, problem=problem, type_queue=QueueFIFO)
