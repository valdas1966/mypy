from __future__ import annotations
from collections import UserList
from f_graph.path.node import NodePath as Node, Cell
from f_core.mixins.comparable import Comparable


class Path(UserList[Node], Comparable):
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

    def reverse(self) -> Path:
        """
        ====================================================================
         Reverse the path.
        ====================================================================
        """
        return Path(data=list(reversed(self.data))) 

    def from_node(self, node: Node) -> Path:
        """
        ====================================================================
         Get the path from the given node to the goal.
        ====================================================================
        """
        return Path(data=self._data[self._data.index(node):])
    
    def key_comparison(self) -> list[Cell]:
        """
        ====================================================================
         Get the key comparison of the path.
        ====================================================================
        """
        return [node.cell for node in self]

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
        nodes = [str(node.cell.to_tuple()) for node in self]
        return '[' + ' -> '.join(nodes) + ']'

    def __eq__(self, other: Path) -> bool:
        """
        ====================================================================
         Compare two paths.
        ====================================================================
        """
        return self.key_comparison() == other.key_comparison()

    @classmethod
    def from_list(cls, nodes: list[Node]) -> Path:
        """
        ====================================================================
         Create a Path from a list of Nodes.
        ====================================================================
        """
        for i in range(len(nodes)):
            if i == 0:
                continue
            nodes[i].parent = nodes[i - 1]
        return cls(data=nodes)
