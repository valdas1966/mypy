from f_graph.path.one_to_one.state import StateOneToOne as State, Node
from f_graph.path.solution import SolutionPath, StatsPath
from f_graph.path.cache import Cache


class SolutionOneToOne(SolutionPath[StatsPath]):
    """
    ============================================================================
     Solution of Path-Algorithm for One-To-One Problem.
    ============================================================================
    """

    def __init__(self,
                 is_valid: bool,
                 state: State,
                 cache: Cache,
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
    def state(self) -> State:
        """
        ========================================================================
         Return the state in the end of the search.
        ========================================================================
        """
        return self._state

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
        best = self._state.best
        path = best.path_from_root()
        path_cached = list()  # Best is Goal
        if best in self._cache:
            path_cached = self._cache[best].path()  # Best is Cached
        path.extend(path_cached)
        return path
