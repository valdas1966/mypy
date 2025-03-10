from __future__ import annotations
from f_ds.graphs.i_1_dict import GraphDict
from f_ds.grids.grid import Grid, Group
from f_ds.nodes.i_2_cell import NodeCell
from typing import Generic, TypeVar, Type, Iterable

Node = TypeVar('Node', bound=NodeCell)


class GraphGrid(Generic[Node], GraphDict[Node]):
    """
    ============================================================================
     Dict-Based {Cell: Node} Graph on 2D-Grids.
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
        keys = grid.to_group().filter(predicate=bool)
        name = name if name else grid.name
        GraphDict.__init__(self, keys=keys, type_node=type_node, name=name)
        self._grid = grid
        self._type_node = type_node

    @property
    def grid(self) -> Grid:
        """
        ========================================================================
         Get the Grid.
        ========================================================================
        """
        return self._grid
    
    def shape(self) -> tuple[int, int]:
        """
        ========================================================================
         Return the Shape of the Grid.
        ========================================================================
        """
        return self._grid.rows, self._grid.cols

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return the Neighbors of the given Node.
        ========================================================================
        """
        return [self.nodes_by_keys(key=cell)
                for cell
                in self._grid.neighbors(cell=node.cell)]
    
    def distance_avg(self, nodes: Iterable[Node]) -> int:
        """
        ========================================================================
         Return the average distance between all the nodes in the iterable.
        ========================================================================
        """
        cells = [node.cell for node in nodes]    
        return self._grid.distance_avg(cells=cells)
    
    def nodes_within_distance(self,
                              node: Node,
                              dist_max: int,
                              dist_min: int = 1) -> Group[Node]:
        """
        ========================================================================
         Return the Nodes within a given Distance-Range.
        ========================================================================
        """
        cells = self._grid.cells_within_distance(cell=node.cell,
                                                 dist_max=dist_max,
                                                 dist_min=dist_min)
        nodes = [self.nodes_by_keys(key=cell) for cell in cells]
        return Group(name='Nodes within Distance',
                     data=nodes)

    def clone(self) -> GraphGrid:
        """
        ========================================================================
         Return a Cloned object.
        ========================================================================
        """
        return type(self)(grid=self._grid,
                          type_node=self._type_node,
                          name=self._name)

    @staticmethod
    def distance(node_a: Node, node_b: Node) -> int:
        """
        ========================================================================
         Return a Manhattan-Distance between two Nodes within the Grid.
        ========================================================================
        """
        cell_a = node_a.cell
        cell_b = node_b.cell
        return Grid.distance(cell_a=cell_a, cell_b=cell_b)

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
