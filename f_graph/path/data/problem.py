from __future__ import annotations
from f_graph.data.problem import ProblemGraph, dataclass
from f_graph.path.elements.graph import GraphPath
from f_graph.path.elements.node import NodePath
from typing import TypeVar

Graph = TypeVar('Graph', bound=GraphPath)
Node = TypeVar('Node', bound=NodePath)


@dataclass(frozen=True)
class ProblemPath(ProblemGraph[Graph, Node]):
    """
    ============================================================================
     ABC of Problem-Path.
    ============================================================================
    """
    start: Node
