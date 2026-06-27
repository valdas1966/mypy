from f_hs.state import StateBase
from f_hs.state.i_1_resource.node_resource import NodeResource
from typing import TypeVar

Node = TypeVar('Node')


class StateResource(StateBase[NodeResource[Node]]):
    """
    ============================================================================
     Search State composing (Node, Resource) into the V×R space for RCSPP.
    ============================================================================
    """

    def __init__(self, key: NodeResource[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        StateBase.__init__(self, key=key)

    @property
    def node(self) -> Node:
        """
        ========================================================================
         Return the underlying Node identity (key.node).
        ========================================================================
        """
        return self.key.node

    @property
    def resource(self) -> int:
        """
        ========================================================================
         Return the Resource level (key.resource).
        ========================================================================
        """
        return self.key.resource
