from __future__ import annotations
from f_core.mixins.iterable import Iterable
from f_ds.graphs.i_1_dict import GraphDict
from f_ds.grids.grid import Grid, Cell, Group
from f_ds.nodes.i_2_cell import NodeCell
from typing import Generic, TypeVar, Type, Iterable

Node = TypeVar('Node', bound=NodeCell)
Graph = TypeVar('Graph', bound='GraphGrid')


class GraphGrid(Generic[Node], GraphDict[Node, Cell]):
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
        uids = grid.to_group().filter(predicate=bool)
        name = name if name else grid.name
        GraphDict.__init__(self, uids=uids, type_node=type_node, name=name)
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
        return [self.nodes_by_uids(uid=cell)
                for cell
                in self._grid.neighbors(cell=node.uid)]
    
    def distance_avg(self, nodes: Iterable[Node]) -> int:
        """
        ========================================================================
         Return the average distance between all the nodes in the iterable.
        ========================================================================
        """
        cells = [node.uid for node in nodes]    
        return self._grid.distance_avg(cells=cells)
    
    def random_nodes_within_distance(self,      
                                     node: Node,
                                     distance_max: int,
                                     distance_min: int = 0,
                                     epochs: int = 1,
                                     n: int = 1) -> set[Node]:
        """
        ========================================================================
         Return a random Node within a given Distance-Range.
        ========================================================================
        """
        func = self._grid.random_cells_within_distance
        cells = func(cell=node.uid,
                     distance_max=distance_max,
                     distance_min=distance_min,
                     epochs=epochs,
                     n=n)
        return set(self.nodes_by_uids(uids=cells))
    
    def random_nodes_within_percentile(self,
                                       node: Node,
                                       percentile_max: int,
                                       percentile_min: int = 0,
                                       epochs: int = 1,
                                       n: int = 1) -> set[Node]:
        """
        ========================================================================
         Return a random Node within a given Percentile-Range.
        ========================================================================
        """
        func = self._grid.random_cells_within_percentile
        cells = func(cell=node.uid,
                     percentile_max=percentile_max,
                     percentile_min=percentile_min,
                     epochs=epochs,
                     n=n)
        return set(self.nodes_by_uids(uids=cells))
    
    def clone(self) -> Graph:
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
        cell_a = node_a.uid
        cell_b = node_b.uid
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
