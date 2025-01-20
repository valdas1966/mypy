from f_graph.problem import ProblemGraph
from f_graph.path.graph import GraphPath as Graph, NodePath as Node


class ProblemPath(ProblemGraph[Graph[Node], Node]):
    """
    ============================================================================
     Problem for Path-Graphs.
    ============================================================================
    """

    def __init__(self, graph: Graph[Node]) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemGraph.__init__(self, graph=graph)
