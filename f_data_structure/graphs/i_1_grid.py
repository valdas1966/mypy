from f_data_structure.graphs.i_0_base import GraphBase
from f_data_structure.f_grid.grid_cells import GridCells as Grid
from f_data_structure.f_grid.cell import Cell
from f_data_structure.nodes.i_2_cell import NodeCell as Node
from typing import Type


class GraphGrid(GraphBase):
    """
    ============================================================================
     Grid-Based Graph.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid,
                 type_node: Type[Node] = Node) -> None:
        GraphBase.__init__(self, name=grid.name)
        self._grid = grid
        self._type_node = type_node
        self._cells_nodes = {cell: type_node(cell=cell)
                             for cell
                             in grid.cells()}

    def get_neighbors(self, node: Node) -> list[Type[Node]]:
        """
        ========================================================================
         Return list of a given Node's neighbors.
        ========================================================================
        """
        return [self.cell_to_node(cell)
                for cell
                in self._grid.neighbors(node.cell)]

    def cell_to_node(self, cell: Cell) -> Type[Node]:
        """
        ========================================================================
         Convert Cell into Node.
        ========================================================================
        """
        return self._cells_nodes[cell]
