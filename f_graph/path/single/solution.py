from f_graph.path.solution import SolutionPath, Node
from f_graph.path.single.components.state import State


class SolutionSingle(SolutionPath):
    """
    ============================================================================
     Solution of Path-Algorithm with Single-Goal.
    ============================================================================
    """

    def __init__(self,
                 state: State,
                 cache: dict[Node, Node],
                 elapsed: int,
                 is_path_found: bool):
        """
        ========================================================================
         Init Attributes.
        ========================================================================
        """
        SolutionPath.__init__(self,
                              elapsed=elapsed,
                              is_path_found=is_path_found)
        self._cache = cache
        self._state = state
        self._path = self._construct_path()

    @property
    def state(self) -> State:
        """
        ========================================================================
         Return the Algo-State at the end of the Search.
        ========================================================================
        """
        return self._state

    @property
    def path(self) -> list[Node]:
        """
        ========================================================================
         Return the Optimal-Path from Start to Goal.
        ========================================================================
        """
        return self._path

    def _construct_path(self) -> list[Node]:
        """
        ========================================================================
         Return a constructed path.
        ========================================================================
        """
        if not self.is_path_found:
            return list()
        path = self.state.best.path_from_start()
        if self.state.best in self._cache:
            best = self.state.best
            path_from_best = self._cache[best].path_from_start()
            path_from_best = list(reversed(path_from_best[:-1]))
            return path + path_from_best
        return path
