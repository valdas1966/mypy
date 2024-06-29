from f_ds.graphs.i_0_base import GraphBase
from f_ds.graphs.nodes.i_2_cell import NodeCell
from f_ds.grids.grid import Grid
from typing import TypeVar, Type

Node = TypeVar('Node', bound=NodeCell)


class GraphGrid(GraphBase[Node]):
    """
    ============================================================================
     Graph represents 2D-Grid.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid,
                 type_node: Type[Node] = NodeCell,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        GraphBase.__init__(self, name)
        self._grid = grid
        self._type_node = type_node
        self._nodes = {cell: type_node(cell=cell)
                       for cell in grid.cells_valid

    @property
    def grid(self) -> Grid:
        return self._grid

    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Return List of Nodes in the Graph.
        ========================================================================
        """
        return list(self._nodes.values())

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Returns a List of a given Node's neighbors.
        ========================================================================
        """
        cells = self._grid.neighbors(node.cell)
        return [self._nodes[cell] for cell in cells]

    def __getitem__(self, index: tuple[int, int]) -> Node:
        """
        ========================================================================
         Direct access to a specific Node using [Row][Col] Properties.
        ========================================================================
        """
        row, col = index
        return self._nodes[self._grid[row][col]]
