from f_ds.graphs.i_0_base import GraphBase, NodeUid
from f_core.abstracts.clonable import Clonable
from abc import abstractmethod
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodeUid)


class ProblemGraph(Generic[Graph, Node], Clonable):
    """
    ============================================================================
     Base-Class for Graph-Problems in Computer Science.
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

    @abstractmethod
    def clone(self) -> Clonable:
        pass
