from f_graph.data.solution import SolutionGraph, dataclass
from f_graph.path.elements.node import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


@dataclass(frozen=True)
class SolutionPath(Generic[Node], SolutionGraph):
    """
    ============================================================================
     ABC for Solution of Path-Problem.
    ============================================================================
    """
    nodes_generated: int
    nodes_explored: int
