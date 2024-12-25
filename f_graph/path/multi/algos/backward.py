from f_graph.path.multi.algo import (AlgoMulti,
                                     ProblemMulti as Problem,
                                     SolutionMulti as Solution)
from f_graph.path.single.algo import AlgoSingle, State as StateSingle, Node
from typing import Type


class Backward(AlgoMulti):
    """
    ============================================================================
     k-Backward Path-Algorithm for Problems with k-Goals.
    ============================================================================
    """

    def __init__(self,
                 problem: Problem,
                 type_algo: Type[AlgoSingle],
                 is_shared: bool,
                 name: str = 'Backward Algo') -> None:
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
         Run the Forward Path-Algorithm (k-Times Single-Algorithm).
        ========================================================================
        """
        solution = Solution()
        state: StateSingle | None = None
        cache: set[Node] = set()
        problems = self._input.to_singles()
        for i, problem in enumerate(problems):
            problem = problem.reverse()
            if not (i and self._is_shared):
                state = StateSingle(type_queue=self._type_algo.type_queue)
            sol_single = self._type_algo(problem=problem,
                                         state=state,
                                         cache=cache).run()
            solution.update(goal=problem.goal,
                            sol_single=sol_single,
                            is_shared=self._is_shared)
            if not sol_single:
                return solution
            if self._is_shared:
                state = sol_single.state
            cache.update(sol_single.path)
        return solution
