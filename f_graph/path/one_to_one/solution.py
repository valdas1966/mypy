from f_graph.path.one_to_one.state import StateOneToOne as State, Node
from f_graph.path.solution import SolutionPath, StatsPath
from f_graph.path.cache import Cache
from f_graph.path.path import Path


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
    def path(self) -> Path:
        """
        ========================================================================
         Return the path of the solution.
        ========================================================================
        """
        return self._path

    def _create_path(self) -> Path:
        """
        ========================================================================
         Return a constructed path.
        ========================================================================
        """
        if not bool(self):
            return list()
        best = self._state.best
        path = Path(data=best.path_from_root())
        # Best is Goal
        if best not in self._cache:
            return path
        # Best is Cached
        path_cached = self._cache[best].path()
        path.extend(path_cached)
        return path
