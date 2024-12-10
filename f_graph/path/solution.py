from f_core.components.data_frozen import DataFrozen, dataclass
from f_graph.path.node import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


@dataclass(frozen=True)
class SolutionPath(Generic[Node], DataFrozen):
    """
    ============================================================================
     ABC for Solution of Path-Problem.
    ============================================================================
    """
    pass
