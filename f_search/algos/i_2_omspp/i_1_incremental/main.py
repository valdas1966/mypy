from f_search.algos.i_1_spp.i_0_base.main import (AlgoSPP, ProblemSPP,
                                                  SolutionSPP, DataSearch)
from f_search.algos.i_2_omspp.i_0_base.main import (AlgoOMSPP, ProblemOMSPP,
                                                    SolutionOMSPP, State)


class AlgoIncremental(AlgoOMSPP):
    """
    ============================================================================
     Iterative Algorithm for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOMSPP,
                 type_algo: type[AlgoSPP],
                 name: str = 'AlgoIncremental',
                 need_path: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        super().__init__(problem=problem, name=name)
        self._need_path = need_path
        self._type_algo = type_algo
        
    def _run(self) -> None:
        """
        ========================================================================
         Run the Algorithm.
        ========================================================================
        """       
        data = DataSearch()
        sub_problems: list[ProblemSPP] = self._problem.to_spps()
        n_problems = len(sub_problems)
        for i, sub_problem in enumerate(sub_problems):
            # Add stats for the goals that were explored during other searches.
            if sub_problem.goal in data.explored:
                path = None
                if self._need_path:
                    path = data.path_to(state=sub_problem.goal)
                solution = SolutionSPP(name_algo=self.name,
                                       is_valid=True, path=path)
                self._sub_solutions[sub_problem.goal] = solution
                continue
            # Run the sub-search.
            name_algo = f'{self._type_algo.__name__} {i+1}/{n_problems}'
            algo = self._type_algo(problem=sub_problem,
                                   data=data,
                                   name=name_algo)
            solution = algo.run()
            self._sub_solutions[sub_problem.goal] = solution
            if not solution:
                # If any subproblem is invalid, the overall solution is invalid
                return self._create_solution()
            # Add Best to Generated (for further searches)
            best = algo.data.best
            cost_best = algo.data.cost[best]
            algo.data.generated.push(state=best, cost=cost_best)
            data = algo.data
        # Return valid solution.
        return self._create_solution()
