from f_data_structure.graphs.i_1_grid import GraphGrid as Graph


class HasGraph:
    """
    ============================================================================
     Mixin-Class for Problems that are represented by a Graph.
    ============================================================================
    """

    def __init__(self, graph: Graph) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._graph = graph

    @property
    def graph(self) -> Graph:
        return self._graph
