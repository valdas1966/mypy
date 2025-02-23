from __future__ import annotations
from collections import UserList
from typing import Iterable
from f_graph.path.node import NodePath as Node


class Path(UserList[Node]):
    """
    ========================================================================
     List of Nodes from Start to Goal.
    ========================================================================
    """

    def __init__(self,
                 data: list[Node]) -> None:
        """
        ====================================================================
         Init private attributes.
        ====================================================================    
        """
        UserList.__init__(self, data)

    @property
    def start(self) -> Node | None:
        """
        ====================================================================
         Get the start node.
        ====================================================================
        """
        return self[0] if self else None

    @property
    def goal(self) -> Node | None:
        """
        ====================================================================
         Get the goal node.
        ====================================================================
        """
        return self[-1] if self else None
    
    def extend(self, other: Path) -> None:
        """
        ====================================================================
         Extend the path.
        ====================================================================
        """
        if self.goal == other.start:
            other.pop(0)
        UserList.extend(self, other)

    def from_node(self, node: Node) -> Path:
        """
        ====================================================================
         Get the path from the given node to the goal.
        ====================================================================
        """
        return Path(data=self._data[self._data.index(node):])

    def __add__(self, other: Path) -> Path:
        """
        ====================================================================
         Add two paths.
        ====================================================================
        """
        path = self.copy()
        path.extend(other)
        return path

    def __getitem__(self, index: int | slice) -> Node | Path:
        """
        ====================================================================
         Get the item at the index or slice (new Path object).
        ====================================================================
        """
        if isinstance(index, int):
            return self.data[index]
        elif isinstance(index, slice):
            return Path(data=self.data[index])
    
    def __reversed__(self) -> Path:
        """
        ====================================================================
         Get the reversed path.
        ====================================================================
        """
        return Path(data=list(reversed(self.data)))

    def __str__(self) -> str:
        """
        ====================================================================
         Get the string representation of the path.
        ====================================================================
        """
        nodes = [str(node.uid.to_tuple()) for node in self]
        return '[' + ' -> '.join(nodes) + ']'
