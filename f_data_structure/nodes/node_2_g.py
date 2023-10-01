from __future__ import annotations
from f_abstract.mixins.parentable import Parentable
from f_data_structure.nodes.node_1_cell import NodeCell


class NodeG(NodeCell):
    """
    ============================================================================
     Node with a weight value (W) and a cost value (G) from the start node.
    ==========================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. is_better_parent(parent: NodeG) -> bool
           [*] Returns True if the given Parent has a lower G-Value than the
                current one.
    ============================================================================
     Inherited Methods:
    ----------------------------------------------------------------------------
        1. distance(other: NodeG) -> int
           [*] Manhattan-Distance between the Nodes.
        2. path_from(other: NodeG) -> list[NodeG]
          [*] Returns a Path from a given Node to the Current.
    ============================================================================
     Magic Methods:
    ----------------------------------------------------------------------------
        1. str -> 'name(row, col)'
        2. repr -> str
        3. eq -> (row, col) == (other.row, other.col)
        4. Comparison funcs based on G-Value.
            An object is considered 'less than' another if its G-Value is
            larger (indicating it is more reliable).
    ============================================================================
    """

    _name: str                        # Node's Name
    _parent: NodeG                    # Node's Parent
    _children: list[NodeG]            # Node's Children
    _row: int                         # Node's Row
    _col: int                         # Node's Col
    _w: int                           # Node's Weight
    _g: int                           # Cost to reach the Node from the Start

    def __init__(self,
                 row: int = 0,
                 col: int = None,
                 name: str = None,
                 parent: NodeG = None,
                 w: int = 1
                 ) -> None:
        NodeCell.__init__(self, row=row, col=col, name=name, parent=parent)
        self._w = w
        self._update_g()

    @property
    def w(self) -> int:
        return self._w

    @property
    def g(self) -> int:
        return self._g

    @Parentable.parent.setter
    def parent(self, parent: NodeG) -> None:
        """
        ========================================================================
         Sets a new Parent and updates the G-Value accordingly.
        ========================================================================
        """
        self._parent = parent
        self._update_g()

    def is_better_parent(self, parent: NodeG) -> bool:
        """
        ========================================================================
         Returns True if the received Parent is better than the current
         (lower G-Value).
        ========================================================================
        """
        return self.g > parent.g + self.w

    def _update_g(self) -> None:
        """
        ========================================================================
         Updates Node's G-Value.
        ========================================================================
        """
        self._g = self.parent.g + self._w if self.parent else 0

    def __lt__(self, other: NodeG) -> bool:
        return self.g > other.g

    def __le__(self, other: NodeG) -> bool:
        return self._g >= other.g

    def __gt__(self, other: NodeG) -> bool:
        return self.g < other.g

    def __ge__(self, other: NodeG) -> bool:
        return self._g <= other.g
