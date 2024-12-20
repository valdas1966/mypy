from __future__ import annotations
from f_graph.data.problem import ProblemGraph, dataclass
from f_graph.path.elements.graph import GraphPath as Graph
from f_graph.path.elements.node import NodePath as Node


@dataclass(frozen=True)
class ProblemPath(ProblemGraph[Graph, Node]):
    """
    ============================================================================
     ABC of Problem-Path.
    ============================================================================
    """
    start: Node
