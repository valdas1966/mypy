from f_ds.queues.i_0_base import QueueBase as Queue
from f_graph.path.state import StatePath, Node
from typing import Type


class StateSingle(StatePath):
    """
    ============================================================================
     State object of Single-Goal Path-Algorithms.
    ============================================================================
    """

    def __init__(self, type_queue: Type[Queue]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StatePath.__init__(self)
        self.generated: type_queue[Node] = type_queue()
        self.explored: set[Node] = set()
        self.best: Node | None = None
