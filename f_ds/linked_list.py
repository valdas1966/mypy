from __future__ import annotations
from f_ds.groups.group import Group
from f_ds.nodes.i_1_prev_next import NodePrevNext, UID
from f_ds.mixins.has_head_tail import HasHeadTail
from f_ds.mixins.groupable import Groupable, Group
from f_core.mixins.has_name import HasName
from typing import Generic, TypeVar


Node = TypeVar('Node', bound=NodePrevNext[UID])


class LinkedList(Generic[Node], Groupable[Node], HasHeadTail[Node, Node], HasName):
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
        HasHeadTail.__init__(self)
        HasName.__init__(self, name=name)

    def prepend(self, node: Node) -> None:
        """
        ========================================================================
         Prepend a node to the head of the Linked-List.
        ========================================================================
        """
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.head.prev = node
            self.head = node

    def prepend_list(self, list: LinkedList[Node]) -> None:
        """
        ========================================================================
         Prepend a list of nodes to the head of the Linked-List.
        ========================================================================
        """
        self.head.prev = list.head
        self.head = list.head

    def append(self, node: Node) -> None:
        """
        ========================================================================
         Append a node to the tail of the Linked-List.
        ========================================================================
        """
        if not self.tail:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def append_list(self, list: LinkedList[Node]) -> None:
        """
        ========================================================================
         Append a list of nodes to the tail of the Linked-List.
        ========================================================================
        """
        self.tail.next = list.head
        self.tail = list.tail

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

