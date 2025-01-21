from f_ds.queues.i_0_base import QueueBase as Queue
from f_graph.path.node import NodePath as Node
from typing import Type


class StateOneToOne:
    """
    ============================================================================
     State object for One-to-One Path-Algorithms.
    ============================================================================
    """

    def __init__(self, type_queue: Type[Queue]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self.generated: type_queue[Node] = type_queue()
        self.explored: set[Node] = set()
        self.best: Node | None = None
