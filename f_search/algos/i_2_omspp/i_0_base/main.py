from f_search.algos.i_0_base import AlgoSearch
from f_search.algos.i_0_base.i_1_best_first import AlgoBestFirst
from f_search.solutions import SolutionOMSPP, SolutionSPP
from f_search.problems import ProblemOMSPP
from f_search.ds.state import StateBase
from f_search.ds.data import DataBestFirst
from typing import Generic, TypeVar
from itertools import islice
from time import time

State = TypeVar('State', bound=StateBase)
Data = TypeVar('Data', bound=DataBestFirst)


class AlgoOMSPP(AlgoSearch[ProblemOMSPP, SolutionOMSPP],
                Generic[State, Data]):
    """
    ============================================================================
     Base for One-to-Many Shortest-Path-Problem Algorithms.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOMSPP,
                 name: str = 'AlgoOMSPP',
                 is_analytics: bool = False,
                 **kwargs) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoSearch.__init__(self,
                            problem=problem,
                            name=name)
        self._is_analytics = is_analytics
        self._goals_active: list[State]
        self._sub_solutions: list[SolutionSPP]

    def _run_pre(self) -> None:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        AlgoSearch._run_pre(self)
        self._goals_active = list(self.problem.goals)
        self._sub_solutions = list()
        self._list_explored: list[dict[str, any]] = list()
        self._dict_bounded_per_goal: dict[State, dict[State, int]] \
            = dict()

    def list_explored(self) -> list[dict[str, any]]:
        """
        ====================================================================
         Return accumulated explored State Data across all sub-searches.
        ====================================================================
        """
        return self._list_explored

    def dict_bounded_per_goal(self) -> dict[State, dict[State, int]]:
        """
        ====================================================================
         Return lower bounds per Goal from bound propagation.
        ====================================================================
        """
        return self._dict_bounded_per_goal

    def _collect_explored(self,
                          goal: State,
                          algo: AlgoBestFirst,
                          offset: int = 0) -> None:
        """
        ====================================================================
         Collect explored State Data from a sub-search Algo.
        ====================================================================
        """
        if not self._is_analytics:
            return
        data = algo._data
        data_cached = getattr(algo, '_data_cached', None)
        dict_h = getattr(data, 'dict_h', None)
        for state in islice(data.explored, offset, None):
            g = data.dict_g.get(state, 0)
            h = dict_h.get(state, 0) if dict_h else 0
            cached = int(state in data_cached.dict_cached) \
                if data_cached else 0
            bounded = int(state in data_cached.dict_bounded) \
                if data_cached else 0
            self._list_explored.append({
                'goal_row': goal.key.row,
                'goal_col': goal.key.col,
                'row': state.key.row,
                'col': state.key.col,
                'f': g + h,
                'cached': cached,
                'bounded': bounded,
                'g': g,
                'h': h
            })

    def closed_categories(self) -> dict[str, list]:
        """
        ========================================================================
         Return CLOSED-list nodes categorized into Surely-Expanded,
          Borderline, and Surplus based on per-goal f-values vs C*_i.
        ========================================================================
        """
        data = self._data
        goals = self.problem.goals
        c_stars = [data.dict_g[goal] for goal in goals]
        surely = list()
        borderline = list()
        surplus = list()
        for state in data.explored:
            g = data.dict_g[state]
            has_surely = False
            all_surplus = True
            for i, goal in enumerate(goals):
                f_i = g + state.distance(other=goal)
                if f_i < c_stars[i]:
                    has_surely = True
                    break
                if f_i == c_stars[i]:
                    all_surplus = False
            if has_surely:
                surely.append(state)
            elif all_surplus:
                surplus.append(state)
            else:
                borderline.append(state)
        return {'Surely Expanded': surely,
                'Borderline': borderline,
                'Surplus': surplus}

    def _create_solution(self) -> SolutionOMSPP:
        """
        ========================================================================
         Construct and return the OMSPP Solution.
        ========================================================================
        """
        elapsed = time() - self._time_start
        return SolutionOMSPP(name_algo=self.name,
                             problem=self.problem,
                             subs=self._sub_solutions,
                             elapsed=elapsed)
