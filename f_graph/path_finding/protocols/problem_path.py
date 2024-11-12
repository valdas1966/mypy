from f_graph.path_finding.protocols.problem_graph import ProtocolProblemGraph, Graph, Node
from typing import Protocol


class ProtocolProblemPath(Protocol[Graph, Node],
                          ProtocolProblemGraph[Graph, Node]):
    """
    ============================================================================
     Protocol for Path-Problems in Computer-Science.
    ============================================================================
    """

    @property
    def start(self) -> Node:
        """
        ========================================================================
         Return the Start-Node of the Problem.
        ========================================================================
        """

    @property
    def goals(self) -> set[Node]:
        """
        ========================================================================
         Return the Goal-Nodes of the Problem.
        ========================================================================
        """
