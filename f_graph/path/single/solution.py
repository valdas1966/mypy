from f_graph.path.solution import SolutionPath, Node
from f_graph.path.single.state import StateSingle as State


class SolutionSingle(SolutionPath[State]):
    """
    ============================================================================
     Solution of Path-Algorithm with Single-Goal.
    ============================================================================
    """

    def __init__(self,
                 is_valid: bool,
                 state: State,
                 cache: dict[Node, Node],
                 elapsed: int) -> None:
        """
        ========================================================================
         Init Attributes.
        ========================================================================
        """
        SolutionPath.__init__(self)
        self._cache = cache
        self._is_valid = is_valid
        self._elapsed = elapsed
        self._state: State = state

    @property
    def path(self) -> list[Node]:
        """
        ========================================================================
         Return a constructed path.
        ========================================================================
        """
        if not bool(self):
            return list()
        path = self.state.best.path_from_start()
        if self.state.best in self._cache:
            best = self.state.best
            path_from_best = self._cache[best].path_from_start()
            path_from_best = list(reversed(path_from_best[:-1]))
            return path + path_from_best
        return path
