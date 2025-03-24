from f_core.components.enum_callable import EnumCallable
from f_ds.queues.i_0_base import QueueBase
from f_ds.queues.i_1_fifo import QueueFIFO
from f_ds.queues.i_1_list import QueueList
from f_graph.path.node import NodePath as Node


class TypeQueue(EnumCallable):
    """
    ============================================================================
     Enum of Type-Queues.
    ============================================================================
    """
    FIFO = QueueFIFO
    PRIORITY = QueueList


class StateOneToOne:
    """
    ============================================================================
     State object for One-to-One Path-Algorithms.
    ============================================================================
    """

    def __init__(self, type_queue: TypeQueue = TypeQueue.PRIORITY) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self.generated: QueueBase[Node] = type_queue()
        self.explored: set[Node] = set()
        self.best: Node | None = None
