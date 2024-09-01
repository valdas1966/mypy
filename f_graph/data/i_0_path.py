from f_ds.queues.i_0_base import QueueBase
from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar, Type
from abc import ABC

Node = TypeVar('Node', bound=NodePath)


class DataPath(ABC, Generic[Node]):
    """
    ============================================================================
     Base-Class of Data for Path-Algorithms (Generated and Explored lists).
    ============================================================================
    """

    def __init__(self, type_queue: Type[QueueBase]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._generated = type_queue[Node]()
        self._explored = set[Node]()

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
