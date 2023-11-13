from __future__ import annotations
from f_data_structure.f_tree.node import Node
from f_data_structure.mixins.has_cost import HasCost


class NodeHasCost(Node, HasCost):
    """
    ============================================================================
     Node with a Cost-Function.
    ============================================================================
    """

    def __init__(self, name: str = None, parent: NodeHasCost = None) -> None:
        """
        ========================================================================
         Initializes the Base-Classes.
        ========================================================================
        """
        Node.__init__(self, name, parent)
        HasCost.__init__(self)

    def __eq__(self, other: NodeHasCost) -> bool:
        return HasCost.__eq__(self, other)

    def __ne__(self, other: NodeHasCost) -> bool:
        return HasCost.__ne__(self, other)
