from f_graph.path.solution import SolutionPath, StatsPath
from f_graph.path.one_to_one.state import State, Node
from typing import Callable


class SolutionOneToOne(SolutionPath[StatsPath]):
    """
    ============================================================================
     Solution of Path-Algorithm for One-To-One Problem.
    ============================================================================
    """

    def __init__(self,
                 is_valid: bool,
                 state: State,
                 cache: dict[Node, Callable[[], list[Node]]],
                 stats: StatsPath) -> None:
        """
        ========================================================================
         Init Attributes.
        ========================================================================
        """
        SolutionPath.__init__(self, is_valid=is_valid, stats=stats)
        self._state = state
        self._cache = cache
        self._path = self._create_path()

    @property
    def path(self) -> list[Node]:
        """
        ========================================================================
         Return the path of the solution.
        ========================================================================
        """
        return self._path

    def _create_path(self) -> list[Node]:
        """
        ========================================================================
         Return a constructed path.
        ========================================================================
        """
        if not bool(self):
            return list()
        best = self.state.best
        start_to_best = self.best.path_from_root()
        best_to_goal = list() # Best is Goal
        if best in self._cache:
            best_to_goal = self._cache[best]() # Best is Cached
        path = start_to_best.extend(best_to_goal)
        return path

    