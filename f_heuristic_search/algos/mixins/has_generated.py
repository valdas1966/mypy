from f_data_structure.collections.i_1_queue import QueueBase
from f_data_structure.nodes.i_0_base import NodeBase
from typing import Generic, TypeVar, Type

Node = TypeVar('Node', bound=NodeBase)


class HasGenerated(Generic[Node]):
    """
    ============================================================================
     Mixin for Algorithms that use list Generated Queue (Open List).
    ============================================================================
    """

    def __init__(self, type_queue: Type[QueueBase]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._generated = type_queue()

    @property
    def generated(self) -> list[Node]:
        return self._generated.elements()
