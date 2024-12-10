from __future__ import annotations
from f_graph.problem import ProblemGraph, dataclass
from f_graph.path.graph import GraphPath
from f_graph.path.node import NodePath
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
