from f_data_structure.nodes.i_0_base import NodeBase
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeBase)


class HasExpanded(Generic[Node]):
    """
    ============================================================================
     Mixin for Algorithms that utilize an already Expanded-Set of Nodes.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._expanded = set[Node]()

    @property
    def expanded(self) -> set[Node]:
        return self._expanded

    def _is_expanded(self, node: Node) -> bool:
        """
        ========================================================================
         Returns True if the given Node was already been expanded.
        ========================================================================
        """
        return node in self._expanded
