from f_data_structure.old_cell import Cell
from f_heuristic_search.nodes.node_g import NodeG
from f_heuristic_search.nodes.node_h import NodeH


class NodeF(NodeG, NodeH):
    """
    ============================================================================
     Desc:
    ----------------------------------------------------------------------------
        1. Represents an Informed-Node with properties for the node's location
           in the grid (Cell), cost tracking from the start node (NodeG), and
           heuristic cost estimate to the goal node (NodeH).
        2. NodeF indeed holds values that provide an estimated representation
           of the node's location in the path between the Start and Goal nodes.
        3. This class overrides Cell's comparison operators to compare nodes by
           its f-values instead of their locations in the grid (like in Cell).
        4. The comparison operators also handles a tie-breaking issue, When two
           nodes have equal f-value, the node with higher g-value is considered
           'smaller' as g-value represents more reliable information about the
           path cost.
    ============================================================================
     Properties:
    ----------------------------------------------------------------------------
        1. f (int)           : Total cost function (g + h).
    ============================================================================
     Inherited Properties:
    ----------------------------------------------------------------------------
        1. name (str)        : Node's Name.
        2. x (int)           : Node's X-Coordinate.
        3. y (int)           : Node's Y-Coordinate.
        4. w (int)           : Weight from the parent to this node.
        5. g (int)           : Cost from the start node to this node.
        6. h (int)           : Heuristic cost from this node to the Goal.
        7. parent (NodeG)    : The predecessor node in the path.
                               (g-value) updates automatically on parent update.
    ============================================================================
        """

    def __init__(self,
                 x: int = None,  # Node's X-Coordinate in the Grid.
                 y: int = None,  # Node's Y-Coordinate in the Grid.
                 name: str = None,  # Node's Name.
                 cell: Cell = None,  # Node's Position in the Grid
                 parent: 'NodeG' = None  # Parent-Node in the Grid.
                 #  None if this is a Start-Node.
                 ) -> None:
        if cell:
            x, y, name = cell.x, cell.y, cell.name
        NodeG.__init__(self, x=x, y=y, name=name, parent=parent)
        NodeH.__init__(self, x=x, y=y, name=name)

    def f(self) -> int:
        return self.g + self.h

    def __lt__(self, other) -> bool:
        """
        ========================================================================
         Desc: Breaks ties first by f-value, then by g-value.
        ========================================================================
        """
        if self.f() < other.f():
            return True
        if self.f() == other.f():
            if self.g > other.g:
                return True
            if self.g == other.g:
                return super().__lt__(other)
        return False

    def __gt__(self, other) -> bool:
        """
        ========================================================================
         Desc: Breaks ties first by f-value, then by g-value.
        ========================================================================
        """
        if self.f() > other.f():
            return True
        if self.f() == other.f():
            if self.g < other.g:
                return True
            if self.g == other.g:
                return super().__gt__(other)
        return False

    def __le__(self, other) -> bool:
        """
        ========================================================================
         Desc: Breaks ties first by f-value, then by g-value.
        ========================================================================
        """
        return self.f() == other.f() or self.__lt__(other)

    def __ge__(self, other) -> bool:
        """
        ========================================================================
         Desc: Breaks ties first by f-value, then by g-value.
        ========================================================================
        """
        return self.f() == other.f() or self.__gt__(other)
