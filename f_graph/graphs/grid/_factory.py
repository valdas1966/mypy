from f_graph.graphs.grid.main import GraphGrid, GridMap


class Factory:
    """
    ============================================================================
     Factory for the GraphGrid.
    ============================================================================
    """

    @staticmethod
    def x() -> GraphGrid:
        """
        ========================================================================
         Return a GraphGrid with a 3x3 grid in a X-Shape.
        ========================================================================
        """
        grid = GridMap.Factory.x()
        return GraphGrid(grid=grid)
