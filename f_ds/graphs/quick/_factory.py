from f_ds.graphs.quick.main import GraphQuick, GridMap


class Factory:
    """
    ============================================================================
     Factory for the GraphQuick.
    ============================================================================
    """

    @staticmethod
    def x() -> GraphQuick:
        """
        ========================================================================
         Return a GraphQuick with a 3x3 grid in a X-Shape.
        ========================================================================
        """
        grid = GridMap.Factory.x()
        return GraphQuick(grid=grid)
