from __future__ import annotations
from f_abstract.mixins.nameable import Nameable
from f_abstract.mixins.hierarchicable import Hierarchicable


class NodeHierarchy(Nameable, Hierarchicable):
    """
    ============================================================================
     Base Node-Class.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. add_child(child: Parentable) -> None
           [*] Adds a Child.
        2. remove_child(child: Parentable) -> None
           [*] Removes a Child from the Children-List.
        3. hierarchical_path_from(other: Hierarchicable) -> List[Hierarchicable]
           [*] Returns a Parent-Hierarchical Path from other Object to Current.
    ============================================================================
    """

    _name: str                               # Node's Name
    _parent: NodeHierarchy                   # Node's Parent
    _children: list[NodeHierarchy]           # Node's Children

    def __init__(self,
                 name: str = None,
                 parent: NodeHierarchy = None) -> None:
        Nameable.__init__(self, name)
        Hierarchicable.__init__(self, parent)
