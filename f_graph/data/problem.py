from f_graph.elements.graphs.i_0_base import GraphBase, NodeGraph
from f_core.components.data_frozen import DataFrozen, dataclass
from f_core.abstracts.clonable import Clonable
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodeGraph)


@dataclass(frozen=True)
class ProblemGraph(Generic[Graph, Node], DataFrozen, Clonable):
    """
    ============================================================================
     Base-Class for Graph-Problems in Computer Science.
    ============================================================================
    """
    graph: Graph
