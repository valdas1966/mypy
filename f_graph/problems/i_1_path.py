from f_graph.problems.i_0_graph import ProblemGraph, GraphBase
from f_graph.nodes.i_1_path import NodePath
from typing import TypeVar

Graph = TypeVar('Graph', bound=GraphBase)
Node = TypeVar('Node', bound=NodePath)


class ProblemPath(ProblemGraph[Graph, Node]):
    """
    ============================================================================
     Graph-Path Problem.
    ============================================================================
    """

    def __init__(self, graph: Graph) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemGraph.__init__(self, graph=graph)
