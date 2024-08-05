from f_abstract.components.data import Data
from f_cs.f_ds.nodes.i_1_path import NodePath
from f_cs.f_ds.collections.i_1_queue import QueueBase
from typing import Generic, TypeVar

Queue = TypeVar('Queue', bound=QueueBase)
Node = TypeVar('Node', bound=NodePath)


class DataPathFindingShortest(Generic[Queue, Node], Data):
    """
    ============================================================================
     Data-Class for Path-Finding algorithm.
    ============================================================================
    """

    def __init__(self) -> None:
        Data.__init__(self)
        self._generated = Queue[Node]()
        self._explored = set[Node]()

    @property
    def generated(self) -> Queue[Node]:
        return self._generated

    @property
    def explored(self) -> set[Node]:
        return self._explored

    def is_generated(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the given Node is already Generated.
        ========================================================================
        """
        return node in self._generated

    def is_explored(self, node: Node) -> bool:
        """
        ========================================================================
         Return True if the given Node is already Explored.
        ========================================================================
        """
        return node in self._explored

    def add_generated(self, node: Node) -> None:
        """
        ========================================================================
         Add list given Node to Generated-Collection.
        ========================================================================
        """
        self._generated.push(element=node)

    def add_explored(self, node: Node) -> None:
        """
        ========================================================================
         Add list given Node to Explored-Collection.
        ========================================================================
        """
        self._explored.add(element=node)
