from f_data_structure.graphs.i_0_base import GraphBase
from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_data_structure.f_grid.cell import Cell
from f_data_structure.nodes.i_1_cell import NodeCell as Node


class GraphGrid(GraphBase):
    """
    ============================================================================
     Grid-Based Graph.
    ============================================================================
    """

    def __init__(self, grid: Grid) -> None:
        GraphBase.__init__(self, name=grid.name)
        self._grid = grid
        self._cells_nodes = {cell: Node(cell) for cell in grid.cells()}

    def get_neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return list of a given Node's neighbors.
        ========================================================================
        """
        return [self._cell_to_node(cell)
                for cell
                in self._grid.neighbors(node.cell)]

    def cell_to_node(self, cell: Cell) -> Node:
        """
        ========================================================================
         Convert Cell into Node.
        ========================================================================
        """
        return self._cells_nodes[cell]
