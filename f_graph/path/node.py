from __future__ import annotations
from f_ds.nodes.i_2_cell import NodeCell, Cell
from f_ds.mixins.has_cache import HasCache
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from f_graph.path.path import Path


class NodePath(NodeCell, HasCache):
    """
    ============================================================================
     Node with a Path functionality.
    ============================================================================
    """

    def __init__(self,
                 key: Cell,
                 parent: NodePath = None,
                 h: int = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        NodeCell.__init__(self, key=key, parent=parent, name=name)
        self._g = 0 if not parent else parent.g + 1
        self._h = h
        self.is_cached = False
        self.is_bounded = False

    @property
    def g(self) -> int:
        """
        ========================================================================
         Get the Path-Cost from the Start to this Node.
        ========================================================================
        """
        return self._g
    
    @property
    def h(self) -> int:
        """
        ========================================================================
         Get the Heuristic-Distance from this Node to the Goal.
        ========================================================================
        """
        return self._h
    
    @h.setter
    def h(self, h: int) -> None:
        """
        ========================================================================
         Set the Heuristic-Distance from this Node to the Goal.
        ========================================================================
        """
        self._h = h

    def f(self) -> int:
        """
        ========================================================================
         Return a Heuristic-Distance from Node to the Goal.
        ========================================================================
        """
        return (self.g + self.h) if self.h is not None else None
    
    def path_from_root(self) -> Path:
        """
        ========================================================================
         Get the Path from the Root to this Node.
        ========================================================================
        """
        from f_graph.path.path import Path 
        nodes = NodeCell.path_from_root(self)
        return Path(data=nodes)
    
    def path_from_node(self, node: NodePath) -> Path:
        """
        ========================================================================
         Get the Path from the given Node to this Node.
        ========================================================================
        """
        from f_graph.path.path import Path
        nodes = NodeCell.path_from_node(self, node=node)
        return Path(data=nodes)

    def key_comparison(self) -> list | Cell:
        """
        ========================================================================
         Compare between Nodes by: F, H, UID.
        ========================================================================
        """
        if self.f() is None:
            return NodeCell.key_comparison(self)
        else:
            return [self.f(),
                    not self.is_cached,
                    not self.is_bounded,
                    -self.g,
                    self.key]
    
    def is_better_parent(self, parent: NodePath) -> bool:
        """
        ========================================================================
         Check if the given parent g-value is better than the current parent.
        ========================================================================
        """
        return self.parent.g > parent.g
    
    def print_details(self) -> None:
        """
        ========================================================================
         Print the Details of the Node.
        ------------------------------------------------------------------------
         Ex: '<cell=(0,0), g=2, h=3, f=5>'
        ========================================================================
        """
        print(f'<cell={self.cell}, g={self.g}, h={self.h}, f={self.f()}, '
              f'is_cached={self.is_cached}, is_bounded={self.is_bounded}> {self.key_comparison()}')
    
    def _update_parent(self) -> None:
        """
        ========================================================================
         Update the Path-Cost from the Start to this Node based on the parent.
        ========================================================================
        """
        self._g = self.parent.g + 1 if self.parent else 0

    def __eq__(self, other: NodePath) -> bool:
        """
        ========================================================================
         Compare two nodes.
        ========================================================================
        """
        return self.key == other.key
    
    def __ne__(self, other: NodePath) -> bool:
        """
        ========================================================================
         Compare two nodes.
        ========================================================================
        """
        return self.key != other.key
    
    def __str__(self) -> str:
        """
        ========================================================================
         Return a STR-Representation of the Node.
        ========================================================================
        """
        return NodeCell.__str__(self)

    def __hash__(self) -> int:
        """
        ========================================================================
         Hash the Node.
        ========================================================================
        """
        return hash(self.key)


