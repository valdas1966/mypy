from __future__ import annotations
from f_data_structure.mixins.hierarchical import Hierarchical
from f_data_structure.nodes.node_0_nameable import NodeNameable


class NodeHierarchical(NodeNameable, Hierarchical):
    """
    ============================================================================
     Represents a Node with a Name and Parent-Children relationship.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        # Hierarchical
    ----------------------------------------------------------------------------
        1. add_child(child: Hierarchical) -> None
           [*] Adds a Child.
        2. remove_child(child: Hierarchical) -> None
           [*] Removes a Child from the Children-List.
        3. path_from_ancestor(other: Hierarchical) -> List[Hierarchical]
           [*] Returns a Parent-Hierarchical Path from other Object to Current.
    ============================================================================
     Inherited Magic Methods:
    ----------------------------------------------------------------------------
        # NameAble
    ----------------------------------------------------------------------------
        1. str() -> str
        2. repr() -> str
        3. hash() -> int
        4. eq() -> bool
        5. ne() -> bool
    ============================================================================
    """

    # NodeNameable
    _name: str                                  # Node's Name
    # Hierarchicable
    _parent: NodeHierarchical                   # Node's Parent
    _children: list[NodeHierarchical]           # Node's Children

    def __init__(self,
                 name: str = None,
                 parent: NodeHierarchical = None) -> None:
        """
        ========================================================================
         Inits the Node's Name and Parent (the children-list starts as empty).
        ========================================================================
        """
        NodeNameable.__init__(self, name)
        Hierarchical.__init__(self, parent)
