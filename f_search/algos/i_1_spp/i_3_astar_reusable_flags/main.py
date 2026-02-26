from f_search.algos.i_1_spp.i_2_astar_reusable.main import (
    AStarReusable, State, Data)
from f_search.problems import ProblemSPP as Problem
from f_search.heuristics import HeuristicsProtocol
from f_search.ds.data.incremental import DataIncremental
from f_search.ds.priority import PriorityGHFlags as Priority
from typing import Generic


class AStarReusableFlags(Generic[State], AStarReusable[State]):
    """
    ========================================================================
     AStar with PriorityGHFlags for Cached/Bounded Heuristic Tiebreaking.
    ========================================================================
     Extends AStarReusable to use PriorityGHFlags instead of PriorityGH.
     States with cached (exact) heuristics are prioritized over bounded
      (lower-bound) heuristics, which are prioritized over unbounded
      (Manhattan) heuristics.
    ========================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: Problem,
                 data_incremental: DataIncremental[State] = None,
                 name: str = 'AStarReusableFlags',
                 data: Data[State] = None,
                 heuristics: HeuristicsProtocol[State] = None,
                 need_path: bool = False
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        AStarReusable.__init__(self,
                               problem=problem,
                               name=name,
                               data=data,
                               heuristics=heuristics)
        self._data_incremental = (data_incremental
                                  if data_incremental
                                  else DataIncremental())
        self._need_path = need_path

    def _discover(self, state: State) -> None:
        """
        ====================================================================
         Discover the given State with flag-aware Priority.
        ====================================================================
        """
        self._stats.discovered += 1
        # Aliases
        data = self._data
        di = self._data_incremental
        # Set State's Parent
        data.set_best_to_be_parent_of(state=state)
        # Determine h-value and flags
        if state in di.dict_cached:
            h = di.dict_cached[state]
            is_cached, is_bounded = True, False
        elif state in di.dict_bounded:
            h = di.dict_bounded[state]
            is_cached, is_bounded = False, True
        else:
            h = self._heuristics(state=state)
            is_cached, is_bounded = False, False
        data.dict_h[state] = h
        # Create Priority with flags
        priority = Priority[State](key=state.key,
                                   g=data.dict_g[state],
                                   h=h,
                                   is_cached=is_cached,
                                   is_bounded=is_bounded)
        data.frontier.push(state=state, priority=priority)

    def _relax(self, succ: State) -> None:
        """
        ====================================================================
         Relax the Successor with flag-aware Priority.
        ====================================================================
        """
        self._stats.relaxed += 1
        # Aliases
        data = self._data
        di = self._data_incremental
        # Set the Successor's Parent to the Best-State
        data.set_best_to_be_parent_of(state=succ)
        # Determine flags (h unchanged, only g changes)
        if succ in di.dict_cached:
            is_cached, is_bounded = True, False
        elif succ in di.dict_bounded:
            is_cached, is_bounded = False, True
        else:
            is_cached, is_bounded = False, False
        # Create Priority with flags
        priority = Priority[State](key=succ.key,
                                   g=data.dict_g[succ],
                                   h=data.dict_h[succ],
                                   is_cached=is_cached,
                                   is_bounded=is_bounded)
        data.frontier.update(state=succ, priority=priority)
