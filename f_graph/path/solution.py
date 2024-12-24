from f_graph.solution import SolutionGraph
from f_graph.path.state import StatePath as State, Node


class SolutionPath(SolutionGraph[Node]):
    """
    ============================================================================
     ABC for Solution of Path-Problem.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        SolutionGraph.__init__(self)
        self._state: State | None = None

    @property
    def state(self) -> State:
        """
        ========================================================================
         Return the State at the end of the Path-Algorithm.
        ========================================================================
        """
        return self._state
