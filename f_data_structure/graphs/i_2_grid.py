from f_data_structure.graphs.i_1_path import GraphPath
from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_data_structure.nodes.i_2_cell import NodeCell as Node


class GraphGrid(GraphPath):
    """
    ============================================================================
     Grid-Based Graph.
    ============================================================================
    """

    def __init__(self, grid: Grid) -> None:
        GraphPath.__init__(self, name=grid.name)
        self._grid = grid
        self._nodes = [Node(cell) for cell in self._grid.cells()]

    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Returns the Graph's Nodes in the Grid's order.
        ========================================================================
        """
        return self._nodes

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return list of a given Node's neighbors.
        ========================================================================
        """
        return [self._nodes[cell]
                for cell
                in self._grid.neighbors(node.cell)
                if not node.parent == self._nodes[cell]]
