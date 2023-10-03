from __future__ import annotations
from f_abstract.mixins.hierarchicable import Hierarchicable
from f_data_structure.nodes.node_0_nameable import NodeNameable


class NodeHierarchy(NodeNameable, Hierarchicable):
    """
    ============================================================================
     Represents a Node with a Name and Parent-Children relationship.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. add_child(child: Parentable) -> None
           [*] Adds a Child.
        2. remove_child(child: Parentable) -> None
           [*] Removes a Child from the Children-List.
        3. path_from_ancestor(other: Hierarchicable) -> List[Hierarchicable]
           [*] Returns a Parent-Hierarchical Path from other Object to Current.
    ============================================================================
    """

    # NodeNameable
    _name: str                               # Node's Name
    # Hierarchicable
    _parent: NodeHierarchy                   # Node's Parent
    _children: list[NodeHierarchy]           # Node's Children

    def __init__(self,
                 name: str = None,
                 parent: NodeHierarchy = None) -> None:
        """
        ========================================================================
         Inits the Node's Name and Parent (the children-list starts as empty).
        ========================================================================
        """
        NodeNameable.__init__(self, name)
        Hierarchicable.__init__(self, parent)
