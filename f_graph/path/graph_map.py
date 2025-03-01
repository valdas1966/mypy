from __future__ import annotations
from f_graph.path.graph import GraphPath, Grid
from f_psl.os.u_path import UPath


class GraphMap(GraphPath):
    """
    ============================================================================
     GraphMap class.
    ============================================================================
    """

    def __init__(self, path: str) -> None:
        """
        ========================================================================
         Initialize the GraphMap by loading the map grid from the given path.
        ========================================================================
        """
        grid = Grid.from_map_grid(path=path)
        GraphPath.__init__(self, grid=grid)
        self._path = path
        self._domain = UPath.last_folder(path)

    def clone(self) -> GraphMap:
        """
        ========================================================================
         Clone the GraphMap.
        ========================================================================
        """
        return GraphMap(path=self._path)

    @property
    def domain(self) -> str:
        """
        ========================================================================
         Get the domain of the graph.
        ========================================================================
        """
        return self._domain
