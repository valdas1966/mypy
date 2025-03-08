from f_ds.nodes.i_0_key import NodeKey, Key
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeKey)


class HasChildren(Generic[Key, Node]):
    """
    ============================================================================
     Mixin-Class for Objects with Children.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._children: dict[Key, Node] = {}

    def children(self) -> dict[K, T]:
        """
        ========================================================================
         Return object's children.
        ========================================================================
        """
        return self._children
    
    def add_child(self, key: K, child: T) -> None:
        """
        ========================================================================
         Add a child to the object.
        ========================================================================
        """
        self._children[key] = child

    def remove_child(self, key: K) -> T:
        """
        ========================================================================
         Remove a child from the object.
        ========================================================================
        """
        return self._children.pop(key)

    def clear_children(self) -> None:
        """
        ========================================================================
         Clear the children of the object.
        ========================================================================
        """
        self._children.clear()
