from f_data_structure.graphs.i_0_base import GraphBase
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)


class HasGraph(Generic[Graph]):
    """
    ============================================================================
     Mixin-Class for Problems that are represented by list Graph.
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
