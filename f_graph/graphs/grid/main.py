from f_core.mixins import HasName, Clonable, Equatable, Dictable
from f_graph.nodes.i_0_key import NodeKey, Key
from f_ds.grids import GridMap
from typing import Generic, TypeVar, Self, Type

Node = TypeVar('Node', bound=NodeKey)


class GraphGrid(Generic[Key, Node],
                Dictable[Key, Node],
                HasName,
                Clonable,
                Equatable):
    """
    ============================================================================
     Grid Graph.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 grid: GridMap,
                 type_node: Type[Node] = NodeKey,
                 name: str = 'GraphGrid') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._grid = grid
        self._type_node = type_node
        data: dict[Key, Node] = dict()
        for cell in grid.cells_valid():
            data[cell] = type_node(key=cell)
        Dictable.__init__(self, data=data)
        HasName.__init__(self, name=name)

    def nodes(self) -> list[Node]:
        """
        ========================================================================
         Return List of Nodes in the Graph.
        ========================================================================
        """
        return list(self.values())

    def neighbors(self, node: Node) -> list[Node]:
        """
        ========================================================================
         Return the neighbors of a node.
        ========================================================================
        """
        cells = self._grid[node.row][node.col]
        return [self[cell] for cell in cells]
    
    @property
    def grid(self) -> GridMap:
        """
        ========================================================================
         Return the Grid.
        ========================================================================
        """
        return self._grid

    def clone(self) -> Self:
        """
        ========================================================================
         Return a Cloned object.
        ========================================================================
        """
        return GraphGrid(grid=self._grid,
                         type_node=self._type_node,
                         name=self.name)

    def key_comparison(self) -> dict[Key, Node]:
        """
        ========================================================================
         Return a Key-Comparison object.
        ========================================================================
        """
        return self.data
    