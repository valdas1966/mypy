from __future__ import annotations
from f_ds.nodes.i_1_prev_next import NodePrevNext
from f_ds.mixins.groupable import Groupable, Group
from f_ds.mixins.has_head import HasHead
from f_core.mixins.has_name import HasName
from f_core.abstracts.clonable import Clonable
from typing import Generic, TypeVar


Node = TypeVar('Node', bound=NodePrevNext)


class LinkedList(Generic[Node],
                 Groupable[Node],
                 HasHead[Node],
                 HasName,
                 Clonable):
    """
    ============================================================================
     A Linked-List.
    ============================================================================
    """

    def __init__(self, name: str = 'Linked-List') -> None:
        """
        ========================================================================
         Initialize the Linked-List.
        ========================================================================
        """
        Groupable.__init__(self)
        HasHead.__init__(self)
        HasName.__init__(self, name=name)
        Clonable.__init__(self)

    def tail(self) -> Node:
        """
        ========================================================================
         Get the Tail of the Linked-List (None if empty).
        ========================================================================
        """
        if not self.head:
            return None
        node = self.head
        while node.next is not None:
            node = node.next
        return node 

    def append(self, node: Node) -> None:
        """
        ========================================================================
         Append a node to the tail of the Linked-List.
        ========================================================================
        """
        # Empty List
        if not self.head:
            self.head = node
        # Non-Empty List
        else:
            tail = self.tail()
            tail.next = node

    def chain(self, node: None, name: str = None) -> LinkedList[Node]:
        """
        ========================================================================
         Chain a node to the tail of the Linked-List.
        ========================================================================
        """
        name = name if name else self.name
        linked = LinkedList(name=name)
        if not self.head:
            linked.head = node
        else:
            linked.head = self.head
            tail = self.tail()
            tail.next = node
        return linked
    
    def clear(self) -> None:
        """
        ========================================================================
         Clear the Linked-List.
        ========================================================================
        """
        self.head = None
    
    def reverse(self, name: str = None) -> LinkedList[Node]:
        """
        ========================================================================
         Return the reverse of the Linked-List.
        ========================================================================
        """
        name = name if name else self.name
        linked = LinkedList(name=name)
        # Empty List
        if not self.head:
            return linked
        # Non-Empty List
        cloned = self.clone()
        li = reversed(list(cloned))
        return LinkedList.from_list(li=li, name=name)
    
    def clone(self, name: str = None) -> LinkedList[Node]:
        """
        ========================================================================
         Clone the Linked-List.
        ========================================================================
        """
        li = [node.clone() for node in self]
        return LinkedList.from_list(li=li, name=name)

    def to_group(self, name: str = None) -> Group[Node]:
        """
        ========================================================================
         Convert the Linked-List to a Group.
        ========================================================================
        """
        data: list[Node] = []
        node: Node = self.head
        while node is not None:
            data.append(node)
            node = node.next
        return Group(name=name, data=data)
    
    @classmethod
    def from_list(cls, li: list[Node], name: str = None) -> LinkedList[Node]:
        """
        ========================================================================
         Create a Linked-List from a list of nodes.
        ========================================================================
        """
        linked = cls(name=name)
        for node in li:
            linked.append(node)
        return linked
    
    def __str__(self) -> str:
        """
        ========================================================================
         Return a string representation of the Linked-List.
        ------------------------------------------------------------------------
         Example: <Linked-List: A -> B -> C>
        ========================================================================
        """
        return f'{self.name}: {" -> ".join((str(x) for x in self)) if self else "None"}'

