from f_graph.path.data.solution import SolutionPath, NodePath, dataclass
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


@dataclass(frozen=True)
class SolutionSingle(Generic[Node], SolutionPath):
    """
    ============================================================================
     Solution of Path-Algorithm with Single-Goal.
    ============================================================================
    """
    path: list[Node]

