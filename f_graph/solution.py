from f_core.mixins.validatable_public import ValidatablePublic
from f_graph.elements.node import NodeGraph
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodeGraph)


class SolutionGraph(Generic[Node], ValidatablePublic):
    """
    ============================================================================
     ABC for Solution of Graph-Problem.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ValidatablePublic.__init__(self)
        self._elapsed: int = 0

    @property
    def elapsed(self) -> int:
        """
        ========================================================================
         Return the Elapsed seconds to reach the Solution.
        ========================================================================
        """
        return self._elapsed

