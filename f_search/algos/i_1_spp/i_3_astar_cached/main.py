from f_search.algos.i_1_spp.i_2_astar_reusable.main import AStarReusable, State
from f_search.problems import ProblemSPP as Problem
from f_search.solutions import SolutionSPP
from f_search.heuristics import HeuristicsProtocol
from f_search.ds.data import DataHeuristics
from f_search.ds.data.cached import DataCached
from f_search.ds.path import Path
from f_search.ds.priority import PriorityGHFlags as Priority
from f_search.utils.propagation import Propagation
from typing import Generic


class AStarCached(Generic[State], AStarReusable[State]):
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
                 heuristics: HeuristicsProtocol[State] = None,
                 data_heuristics: DataHeuristics[State] = None,
                 data_cached: DataCached[State] = None,
                 need_path: bool = False,
                 name: str = 'AStarCached',
                 ) -> None:
        """
        ====================================================================
         Init private Attributes.
        ====================================================================
        """
        AStarReusable.__init__(self,
                               problem=problem,
                               name=name,
                               data=data_heuristics,
                               heuristics=heuristics)
        self._data_cached = data_cached or DataCached()
        self._need_path = need_path

    @property
    def reached_goal(self) -> bool:
        """
        ====================================================================
         Return True if the search reached the Goal (not early cached
          termination).
        ====================================================================
        """
        return self._data.best == self.problem.goal

    def _can_terminate(self) -> bool:
        """
        ====================================================================
         Return True if the Best-State is the Goal or has a cached
          (exact) heuristic.
        ====================================================================
        """
        best = self._data.best
        if best == self.problem.goal:
            return True
        return best in self._data_cached.dict_cached

    def _run(self) -> SolutionSPP:
        """
        ====================================================================
         Run the Algorithm and return the Solution.
        ====================================================================
        """
        if not self._data.frontier:
            self._discover(state=self.problem.start)
        while self._should_continue():
            self._select_best()
            if self._can_terminate():
                break
            self._explore_best()
        is_valid = self._can_terminate()
        path = None
        if self._need_path and is_valid:
            best = self._data.best
            path = self._data.path_to(state=best)
            # Extend path through cached parents to the goal
            if best != self.problem.goal:
                extension = []
                cur = self._data_cached.dict_parent.get(best)
                while cur is not None:
                    extension.append(cur)
                    cur = self._data_cached.dict_parent.get(cur)
                path = path + Path(states=extension)
        return SolutionSPP(name_algo=self.name,
                           problem=self.problem,
                           is_valid=is_valid,
                           path=path,
                           stats=self._stats)

    def distances_to_goal(self) -> dict[State, int]:
        """
        ====================================================================
         Return exact distances to Goal for States on the optimal Path.
        ====================================================================
        """
        path = self._data.path_to(state=self.problem.goal)
        g_goal = self._data.dict_g[self.problem.goal]
        return {s: g_goal - self._data.dict_g[s] for s in path}

    def bounds_to_goal(self) -> dict[State, int]:
        """
        ====================================================================
         Return lower bounds on distance to Goal for explored non-path
          States.
        ====================================================================
        """
        path = set(self._data.path_to(state=self.problem.goal))
        g_goal = self._data.dict_g[self.problem.goal]
        return {s: g_goal - self._data.dict_g[s]
                for s in self._data.explored
                if s not in path}

    def propagate_bounds(self, depth: int) -> dict[State, int]:
        """
        ====================================================================
         Propagate bounds to unvisited neighbors via multi-source BFS.
        ====================================================================
        """
        bounds = self.bounds_to_goal()
        if not depth:
            return bounds
        sources = {**bounds, **self.distances_to_goal()}
        propagation = Propagation(sources=sources,
                                  excluded=set(sources.keys()),
                                  successors=self.problem.successors,
                                  depth=depth,
                                  prune=self._heuristics)
        bounds.update(propagation.run())
        return bounds

    def list_explored(self) -> list[dict[str, any]]:
        """
        ====================================================================
         Return a list of dicts for each explored State with:
          row, col, f, is_cached, is_bounded, g, h.
        ====================================================================
        """
        rows = []
        for state in self._data.explored:
            d = self._data.data_state(state=state)
            di = self._data_cached.data_state(state=state)
            rows.append({'row': state.key.row,
                         'col': state.key.col,
                         'f': d['f'],
                         'is_cached': int(di['is_cached']),
                         'is_bounded': int(di['is_bounded']),
                         'g': d['g'],
                         'h': d['h']})
        return rows

    def _discover(self, state: State) -> None:
        """
        ====================================================================
         Discover the given State with flag-aware Priority.
        ====================================================================
        """
        self._stats.discovered += 1
        # Aliases
        data = self._data
        di = self._data_cached
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
        di = self._data_cached
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
