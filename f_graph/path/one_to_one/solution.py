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
                 is_valid: bool = True,
                 state: State = None,
                 cache: Cache = None,
                 stats: StatsPath = None,
                 goal: Node = None) -> None:
        """
        ========================================================================
         Init Attributes.
        ========================================================================
        """
        self._cache = cache
        self._state = state
        if goal:
            stats = StatsPath()
        SolutionPath.__init__(self, is_valid=is_valid, stats=stats)
        self._path = goal.path_from_root() if goal else self._create_path()
        

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
            return Path(data=list())
        best = self._state.best
        path = best.path_from_root()
        # Best is Goal
        if best not in self._cache:
            return path
        # Best is Cached
        path_cached = self._cache[best]
        path.extend(path_cached)
        return path
