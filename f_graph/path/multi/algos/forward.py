from f_graph.path.multi.algo import (AlgoMulti, ProblemMulti, SolutionMulti)
from f_graph.path.single.algo import (AlgoSingle, Solution as SolutionSingle,
                                      State as StateSingle, Node)
from typing import Type


class ForwardMulti(AlgoMulti):
    """
    ============================================================================
     k-Forward Path-Algorithm for Problems with k-Goals.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemMulti,
                 type_algo: Type[AlgoSingle],
                 is_shared: bool,
                 name: str = 'Forward Algo') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoMulti.__init__(self, problem=problem, name=name)
        self._type_algo = type_algo
        self._is_shared = is_shared

    def run(self) -> SolutionMulti:
        """
        ========================================================================
         Run the Forward Path-Algorithm (k-Times Single-Algorithm).
        ========================================================================
        """
        solutions: dict[Node, SolutionSingle] = dict()
        state: StateSingle | None = None
        problems = self._input.to_singles()
        for i, problem in enumerate(problems):
            if not (i and self._is_shared):
                state = StateSingle(type_queue=self._type_algo.type_queue)
            solution = self._type_algo(problem=problem, state=state).run()
            solutions[problem.goal] = solution
            if not solution:
                return SolutionMulti(solutions=solutions)
            if self._is_shared:
                state = solution.state
                state.unpop_best()
        return SolutionMulti(solutions=solutions)
