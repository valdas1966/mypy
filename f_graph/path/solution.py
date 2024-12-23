from f_graph.solution import SolutionGraph
from f_graph.path.elements.node import NodePath as Node


class SolutionPath(SolutionGraph[Node]):
    """
    ============================================================================
     ABC for Solution of Path-Problem.
    ============================================================================
    """

    def __init__(self, elapsed: int, is_path_found: bool) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionGraph.__init__(self, elapsed=elapsed)
        self._is_path_found = is_path_found

    @property
    def is_path_found(self) -> bool:
        """
        ========================================================================
         Return True if the Path was found.
        ========================================================================
        """
        return self._is_path_found
