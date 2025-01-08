from __future__ import annotations
from f_core.abstracts.clonable import Clonable
from f_graph.problem import ProblemGraph
from f_graph.path.graph import GraphPath as Graph
from f_ds.nodes.i_1_heuristic import NodeHeuristic as Node
from abc import abstractmethod


class ProblemPath(ProblemGraph[Graph, Node]):
    """
    ============================================================================
     ABC of Problem-Path.
    ============================================================================
    """

    def __init__(self, graph: Graph, start: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ProblemGraph.__init__(self, graph=graph)
        self._start = start

    @property
    def start(self) -> Node:
        """
        ========================================================================
         Return a Start-Node of the Problem.
        ========================================================================
        """
        return self._start

    @abstractmethod
    def clone(self) -> Clonable:
        pass
