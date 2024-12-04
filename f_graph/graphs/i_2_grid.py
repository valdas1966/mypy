from __future__ import annotations
from f_graph.graphs.i_1_dict import GraphDict
from f_graph.node import NodeGraph
from f_ds.grids.grid import Grid, Cell
from typing import Generic, TypeVar, Type

Node = TypeVar('Node', bound=NodeGraph)


class GraphGrid(Generic[Node], GraphDict[Node, Cell]):
    """
    ============================================================================
     Dict-Based {Cell: Node} Graph on 2D-Grids.
    ============================================================================
    """

    def __init__(self,
                 grid: Grid,
                 type_node: Type[Node],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        uids = grid.to_group().filter(predicate=bool)
        GraphDict.__init__(self, uids=uids, type_node=type_node, name=name)
        self._grid = grid
        self._type_node = type_node

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return the Neighbors of the given Node.
        ========================================================================
        """
        return [self.node_from_uid(uid=cell)
                for cell
                in self._grid.neighbors(cell=node.uid)]

    def clone(self) -> GraphGrid:
        """
        ========================================================================
         Return a Cloned object.
        ========================================================================
        """
        return GraphGrid(grid=self._grid,
                         type_node=self._type_node,
                         name=self._name)

    def __getitem__(self, index: tuple[int, int]) -> Node:
        """
        ========================================================================
         Direct access to a Node using Row and Col of it's Cell.
        ========================================================================
        """
        row, col = index
        return self._nodes[self._grid[row][col]]

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-Repr of the Grid.
        ========================================================================
        """
        return str(self._grid)
