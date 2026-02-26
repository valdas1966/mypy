from f_search.algos.i_1_spp.i_1_astar.main import (AStar, State, Data,
                                                    Priority, Frontier)
from f_search.problems import ProblemSPP as Problem
from f_search.heuristics import HeuristicsProtocol, HeuristicsManhattan as Manhattan
from f_search.utils.propagation import Propagation
from typing import Generic


class AStarReusable(Generic[State], AStar[State]):
    """
    ============================================================================
     AStar with reusable Data for chaining searches.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 problem: Problem,
                 name: str = 'AStarReusable',
                 data: Data[State] = None,
                 heuristics: HeuristicsProtocol[State] = None,
                 need_path: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AStar.__init__(self, problem=problem, name=name)
        if data:
            self._data = data
        if heuristics:
            self._heuristics = heuristics
        self._need_path = need_path

    def distances_to_goal(self) -> dict[State, int]:
        """
        ========================================================================
         Return exact distances to Goal for States on the optimal Path.
        ========================================================================
        """
        path = self._data.path_to(state=self.problem.goal)
        g_goal = self._data.dict_g[self.problem.goal]
        return {s: g_goal - self._data.dict_g[s] for s in path}

    def bounds_to_goal(self) -> dict[State, int]:
        """
        ========================================================================
         Return lower bounds on distance to Goal for explored non-path States.
        ========================================================================
        """
        path = set(self._data.path_to(state=self.problem.goal))
        g_goal = self._data.dict_g[self.problem.goal]
        return {s: g_goal - self._data.dict_g[s]
                for s in self._data.explored
                if s not in path}

    def propagate_bounds(self, depth: int) -> dict[State, int]:
        """
        ========================================================================
         Propagate bounds to unvisited neighbors via multi-source BFS.
        ========================================================================
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
