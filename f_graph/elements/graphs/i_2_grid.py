from __future__ import annotations
from f_graph.elements.graphs.i_1_dict import GraphDict
from f_graph.elements.node import NodeGraph
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
        return [self.node(uid=cell)
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

    @staticmethod
    def distance(node_a: Node, node_b: Node) -> int:
        """
        ========================================================================
         Return a Manhattan-Distance between two Nodes within the Grid.
        ========================================================================
        """
        cell_a = node_a.uid
        cell_b = node_b.uid
        return Grid.distance(cell_a=cell_a, cell_b=cell_b)

    @classmethod
    def gen(cls,
            rows: int,
            cols: int = None,
            pct_valid: int = 100,
            type_node: Type[NodeGraph] = NodeGraph,
            name: str = None) -> GraphGrid:
        """
        ========================================================================
         Return a generated GraphGrid with custom Params.
        ========================================================================
        """
        grid = Grid.generate(rows=rows, cols=cols, pct_valid=pct_valid)
        return cls(grid=grid, type_node=type_node, name=name)

    @classmethod
    def gen_3x3(cls,
                type_node: Type[NodeGraph] = NodeGraph,
                name: str = None) -> GraphGrid:
        """
        ========================================================================
         Generate a 3x3 Full-GraphGrid.
        ========================================================================
        """
        grid = Grid.generate(rows=3)
        return cls(grid=grid, type_node=type_node, name=name)

    @classmethod
    def gen_4x4(cls,
                type_node: Type[NodeGraph] = NodeGraph,
                name: str = None) -> GraphGrid:
        grid = Grid.generate(rows=4)
        Cell.invalidate([grid[0][2], grid[1][2]])
        return cls(grid=grid, type_node=type_node, name=name)

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
