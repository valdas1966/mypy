from f_graph.path.solution import SolutionPath, Node
from f_graph.path.single.state import State


class SolutionSingle(SolutionPath):
    """
    ============================================================================
     Solution of Path-Algorithm with Single-Goal.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init Attributes.
        ========================================================================
        """
        SolutionPath.__init__(self)
        self._cache = cache
        self.state = state
        self._path = self._construct_path()

    @property
    def path(self) -> list[Node]:
        """
        ========================================================================
         Return the Optimal-Path from Start to Goal.
        ========================================================================
        """
        return self._path
