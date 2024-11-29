from __future__ import annotations
from f_graph.graphs.i_0_base import GraphBase
from f_graph.nodes.i_1_path_cell import NodePathCell
from f_ds.grids.grid import Grid, Cell
from typing import TypeVar, Type

Node = TypeVar('Node', bound=NodePathCell)


class GraphGrid(GraphBase[Node]):
    """
    ============================================================================
     Graph represents 2D-Grid.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid,
                 type_node: Type[Node] = NodePathCell,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        GraphBase.__init__(self, name)
        self._grid = grid
        self._type_node = type_node
        self._nodes: dict[Cell, Node] = self._map_cells_to_nodes()

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

    def children(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return List of Node's neighbors that are not its parents.
        ========================================================================
        """
        return [child
                for child
                in self.neighbors(node=node)
                if child.parent != node]

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Returns List of Node's neighbors.
        ========================================================================
        """
        cells = self._grid.neighbors(node.cell)
        return [self._nodes[cell] for cell in cells]

    def distance(self,
                 node_a: Node,
                 node_b: Node) -> int:
        """
        ========================================================================
         Return Manhattan-Distance between 2 Nodes.
        ========================================================================
        """
        cell_a = node_a.cell
        cell_b = node_b.cell
        return self._grid.distance(cell_a, cell_b)

    def copy(self) -> GraphGrid:
        """
        ========================================================================
         Return a new instance of Graph with reset Nodes.
        ========================================================================
        """
        return GraphGrid[Node](grid=self._grid,
                               type_node=self._type_node,
                               name=self._name)

    def _map_cells_to_nodes(self) -> dict[Cell, Node]:
        """
        ========================================================================
         Return a Dict that maps Cells to their represented Nodes.
        ========================================================================
        """
        return {cell: self._type_node(cell=cell)
                for cell
                in self._grid.to_group()
                if cell}

    def __getitem__(self, index: tuple[int, int]) -> Node:
        """
        ========================================================================
         Direct access to list specific Node using [Row][Col] Properties.
        ========================================================================
        """
        row, col = index
        return self._nodes[self._grid[row][col]]
