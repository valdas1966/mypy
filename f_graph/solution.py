from f_graph.elements.node import NodeGraph
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeGraph)


class SolutionGraph(Generic[Node]):
    """
    ============================================================================
     ABC for Solution of Graph-Problem.
    ============================================================================
    """

    def __init__(self, elapsed: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._elapsed = elapsed

    @property
    def elapsed(self) -> int:
        """
        ========================================================================
         Return an Elapsed seconds to Algo solve the Problem.
        ========================================================================
        """
        return self._elapsed
