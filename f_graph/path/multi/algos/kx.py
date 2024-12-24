from f_graph.path.multi.algo import AlgoMulti, ProblemMulti, SolutionMulti
from f_graph.path.multi.state import StateMulti
from f_graph.path.single.algo import (AlgoSingle, Solution as SolutionSingle,
                                      Node)
from typing import Type


class KX(AlgoMulti):

    def __init__(self,
                 problem: ProblemMulti,
                 type_algo: Type[AlgoSingle],
                 name: str = 'KX Algo') -> None:
        """
        ========================================================================
         ABC for Multiple-Goals Path-Algorithms with K-Iterations.
        ========================================================================
        """
        AlgoMulti.__init__(self, problem=problem, name=name)
        self._type_algo = type_algo
        self._paths: dict[Node, list[Node]] = dict()
        self._elapsed = 0
        self._state = StateMulti()

    def run(self) -> SolutionMulti:
        problems = self._input.to_singles()
        for problem in problems:
            algo_single = self._type_algo(problem=problem)
            sol_single = algo_single.run()
            if not sol_single:
                return self._create_solution(is_valid=False)

        return SolutionMulti(is_valid=True,
                             elapsed=elapsed,
                             state=state,
                             paths=paths)

    def _create_solution(self, is_valid: bool) -> SolutionMulti:
        return SolutionMulti(is_valid=is_valid,
                             state=self._state,
                             elapsed=self._elapsed,
                             paths=self._paths)

    def _update_solution(self, sol_single: SolutionSingle) -> None:
        self._state.add_generated(sol_single.state.generated.to_iterable())
        self._state.add_explored(sol_single.state.explored)
        self._elapsed += sol_single.elapsed
        self._paths[self._input.goal] = sol_single.path
