from f_graph.path.multi.algo import AlgoMulti, ProblemMulti, SolutionMulti
from f_graph.path.one_to_one.algo import AlgoOneToOne, SolutionSingle, Node
from typing import Type


class BackwardMulti(AlgoMulti):
    """
    ============================================================================
     k-Backward Path-Algorithm for Problems with k-Goals.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemMulti,
                 type_algo: Type[AlgoOneToOne],
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

    def run(self) -> SolutionMulti:
        """
        ========================================================================
         Run the Forward Path-Algorithm (k-Times Single-Algorithm).
        ========================================================================
        """
        solutions_single: dict[Node, SolutionSingle] = dict()
        cache: set[Node] = set()
        problems = self._input.to_singles()
        for i, problem in enumerate(problems):
            problem = problem.reverse()
            if not self._is_shared:
                solution_single = self._type_algo(problem=problem).run()
                solutions_single[problem.goal] = solution_single
                if not solution_single:
                    return SolutionMulti(solutions=solutions_single,
                                         is_shared=self._is_shared)
        return SolutionMulti(solutions=solutions_single,
                             is_shared=self._is_shared)

