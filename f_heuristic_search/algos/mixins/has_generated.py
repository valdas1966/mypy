from f_data_structure.collections.base.i_1_queue import QueueBase
from f_data_structure.nodes.i_0_base import NodeBase
from typing import Generic, TypeVar, Type

Node = TypeVar('Node', bound=NodeBase)


class HasGenerated(Generic[Node]):
    """
    ============================================================================
     Mixin for Algorithms that use a Generated (Open) List.
    ============================================================================
    """

    def __init__(self, type_queue: Type[QueueBase[Node]]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._generated = type_queue[Node]()

    @property
    def generated(self) -> list[Node]:
        return self._generated.elements()

    def _is_generated(self, node: Node) -> bool:
        """
        ========================================================================
         Returns True if the given Node was already generated.
        ========================================================================
        """
        return node in self._generated
