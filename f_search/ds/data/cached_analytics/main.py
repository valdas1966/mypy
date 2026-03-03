from f_search.ds.data.i_1_heuristics import DataHeuristics
from f_search.ds.data.cached import DataCached
from f_search.ds.state import StateBase
from typing import TypeVar, Generic

State = TypeVar('State', bound=StateBase)


class DataCachedAnalytics(Generic[State]):
    """
    ========================================================================
     Analytics Data collected from Incremental Backward sub-searches.
    ========================================================================
     Collects explored State's Data across all sub-searches, merging
      DataHeuristics (key, f, g, h) and DataCached (is_cached,
      is_bounded) with the sub-search goal.
    ========================================================================
    """

    def __init__(self) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        self._list_explored: list[dict[str, any]] = []

    @property
    def list_explored(self) -> list[dict[str, any]]:
        """
        ====================================================================
         Return the list of explored States with their Data.
        ====================================================================
        """
        return self._list_explored

    def collect(self,
                goal_key: any,
                data: DataHeuristics[State],
                data_cached: DataCached[State]) -> None:
        """
        ====================================================================
         Collect explored State's Data from a completed sub-search.
        ====================================================================
        """
        for state in data.explored:
            d = data.data_state(state)
            di = data_cached.data_state(state)
            row = {
                'goal': goal_key.key,
                'key': state.key.key,
                'f': d['f'],
                'g': d['g'],
                'h': d['h'],
                'is_cached': int(di['is_cached']),
                'is_bounded': int(di['is_bounded']),
            }
            self._list_explored.append(row)
