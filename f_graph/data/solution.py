from f_core.components.data_frozen import DataFrozen, dataclass
from f_graph.elements.node import NodeGraph
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeGraph)


@dataclass(frozen=True)
class SolutionGraph(Generic[Node], DataFrozen):
    """
    ============================================================================
     ABC for Solution of Graph-Problem.
    ============================================================================
    """
    elapsed: int
