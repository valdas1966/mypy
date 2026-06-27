from f_core.mixins import Tupleable
from typing import Generic, TypeVar

Node = TypeVar('Node')


class NodeResource(Tupleable, Generic[Node]):
    """
    ============================================================================
     Composite (Node, Resource) identity for Resource-Constrained Search.
    ============================================================================
    """

    def __init__(self, node: Node, resource: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._node = node
        self._resource = resource

    @property
    def node(self) -> Node:
        """
        ========================================================================
         Return the underlying Node identity.
        ========================================================================
        """
        return self._node

    @property
    def resource(self) -> int:
        """
        ========================================================================
         Return the Resource level.
        ========================================================================
        """
        return self._resource

    def to_tuple(self) -> tuple[Node, int]:
        """
        ========================================================================
         Return (Node, Resource) — the identity tuple.
        ========================================================================
        """
        return self._node, self._resource
