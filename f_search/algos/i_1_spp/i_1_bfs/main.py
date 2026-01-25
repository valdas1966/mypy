from f_search.algos.i_0_base.i_1_best_first import AlgoBestFirst
from f_search.problems import ProblemSPP as Problem
from f_search.solutions import SolutionSPP as Solution
from f_search.stats import StatsSearch as Stats
from f_search.ds.data import DataBestFirst as Data
from f_search.ds.state import StateBase as State


class BFS(AlgoBestFirst[Problem, Solution, Stats, Data]):

    def run(self) -> Solution:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._run_pre()
        # If incremental algorithm
        if self._data.generated:
            self._update_generated()
        else:
            # If not incremental algorithm
            self._generate_state(state=self._problem.start)
        while self._should_continue():
            self._update_best()
            if self._can_terminate():
                return self._create_solution(is_valid=True)
            self._explore_best()
        return self._create_solution(is_valid=False)