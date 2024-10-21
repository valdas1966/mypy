from f_ds.queues.i_0_base import QueueBase
from f_ds.queues.i_1_fifo import QueueFIFO
from f_ds.queues.i_1_priority import QueuePriority
from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar
from enum import Enum
from abc import ABC

Node = TypeVar('Node', bound=NodePath)


class TypeQueue(Enum):
    """
    ============================================================================
     Enum for Queues-Types enables as Generated object.
    ============================================================================
    """
    FIFO = QueueFIFO
    PRIORITY = QueuePriority


class DataPath(ABC, Generic[Node]):
    """
    ============================================================================
     Base-Class of Data for Path-Algorithms (Generated and Explored lists).
    ============================================================================
    """

    def __init__(self, type_queue: TypeQueue) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._generated = type_queue.value()
        self._explored = set()

    @property
    def generated(self) -> QueueBase[Node]:
        """
        ========================================================================
         Return list Queue of generated nodes.
        ========================================================================
        """
        return self._generated

    @property
    def explored(self) -> set[Node]:
        """
        ========================================================================
         Return list Set of explored nodes.
        ========================================================================
        """
        return self._explored
