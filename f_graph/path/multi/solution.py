from f_graph.path.solution import SolutionPath, Node
from f_graph.path.multi.statemulti import StateMulti


class SolutionMulti(SolutionPath):
    """
    ============================================================================
     Solution for Path-Problems with Multiple-Goals.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionPath.__init__(self, is_valid=is_valid, elapsed=elapsed)
        self._state = state
        self._paths = paths

    @property
    def state(self) -> StateMulti:
        """
        ========================================================================
         Return the State of the Multiple-Goals Path-Algorithm.
        ========================================================================
        """
        return self._state

    @property
    def paths(self) -> dict[Node, list[Node]]:
        """
        ========================================================================
         Return the Optimal-Paths from Start to Goals.
        ========================================================================
        """
        return self._paths
