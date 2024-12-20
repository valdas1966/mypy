from f_graph.data.solution import SolutionGraph, dataclass
from f_graph.path.elements.node import NodePath as Node


@dataclass(frozen=True)
class SolutionPath(SolutionGraph[Node]):
    """
    ============================================================================
     ABC for Solution of Path-Problem.
    ============================================================================
    """
    is_path_found: bool
