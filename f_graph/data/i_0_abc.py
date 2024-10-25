from f_ds.queues.i_0_base import QueueBase
from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar, Type
from abc import ABC

Node = TypeVar('Node', bound=NodePath)


class DataABC(ABC, Generic[Node]):
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
        self._generated = type_queue()
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

    def mark_generated(self, node: Node) -> None:
        """
        ========================================================================
         Mark a Node as Generated.
        ========================================================================
        """
        self._generated.push(item=node)

    def mark_explored(self, node: Node) -> None:
        """
        ========================================================================
         Mark a Node as Explored.
        ========================================================================
        """
        self._explored.add(node)

    def is_generated(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Node was Generated.
        ========================================================================
        """
        return node in self._generated

    def is_explored(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the Node was Explored.
        ========================================================================
        """
        return node in self._explored
