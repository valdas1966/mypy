from f_graph.path.multi.algo import (AlgoMulti,
                                     ProblemMulti as Problem,
                                     SolutionMulti as Solution)
from f_graph.path.single.algo import AlgoSingle, State as StateSingle
from typing import Type


class Iterative(AlgoMulti):
    """
    ============================================================================
     k-Iterative Path-Algorithm for Problems with k-Goals.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_algo: Type[AlgoSingle],
                 is_shared: bool,
                 name: str = 'Iterative Algo') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoMulti.__init__(self, problem=problem, name=name)
        self._type_algo = type_algo
        self._is_shared = is_shared

    def run(self) -> Solution:
        """
        ========================================================================
         Run the Iterative Path-Algorithm (k-Times Single-Algorithm).
        ========================================================================
        """
        solution = Solution()
        state: StateSingle | None = None
        problems = self._input.to_singles()
        for i, problem in enumerate(problems):
            if not (i and self._is_shared):
                state = StateSingle(type_queue=self._type_algo.type_queue)
            sol_single = self._type_algo(problem=problem, state=state).run()
            solution.update(goal=problem.goal,
                            sol_single=sol_single,
                            is_shared=self._is_shared)
            if not sol_single:
                return solution
            if self._is_shared:
                state = sol_single.state
            print(f'{self._is_shared}, Explored={len(state.explored)}, {len(solution.state.explored)}')
        return solution
