from f_ds.graphs.i_1_dict import GraphDict


class GenGraphDict:
    """
    ============================================================================
     Generator for Dict-Based Graphs.
    ============================================================================
    """

    @staticmethod
    def one() -> GraphDict:
        """
        ========================================================================
         Generate a Graph with 1 Node.
        ========================================================================
        """
        return GraphDict(keys=[1])

    @staticmethod
    def two() -> GraphDict:
        """
        ========================================================================
         Generate a Graph with 2 Nodes.
        ========================================================================
        """
        keys = (1, 2)
        return GraphDict(keys=keys)
