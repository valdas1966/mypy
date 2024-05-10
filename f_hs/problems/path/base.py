from f_hs.problems.base import ProblemGraph, GraphBase
from f_ds.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodePath)

class ProblemPath(Generic[Graph, Node], ProblemGraph[Graph, Node]):
    """
    ============================================================================
     Base-Class for Path-Finding problems in Graph-Problems.
    ============================================================================
    """

    def __init__(self, graph: Graph) -> None:
        ProblemGraph.__init__(self, graph=graph)
