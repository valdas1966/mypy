from f_search.algos.i_1_spp.i_0_base.main import (AlgoSPP, ProblemSPP,
                                                  SolutionSPP, DataSPP)
from f_search.algos.i_2_omspp.i_0_base.main import (AlgoOMSPP, ProblemOMSPP,
                                                    SolutionOMSPP, State)


class IterativeOMSPP(AlgoOMSPP):
    """
    ============================================================================
     Iterative Algorithm for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """
    
    # Factory
    Factory: type = None

    def __init__(self,
                 problem: ProblemOMSPP,
                 type_algo: type[AlgoSPP],
                 verbose: bool = False,
                 name: str = 'IterativeOMSPP') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        AlgoOMSPP.__init__(self,
                           problem=problem,
                           verbose=verbose,
                           name=name)
        self._type_algo = type_algo
        
    def run(self) -> SolutionOMSPP:
        """
        ========================================================================
         Run the Algorithm and return the Solution.
        ========================================================================
        """
        self._run_pre()       
        data = DataSPP() 
        sub_problems: list[ProblemSPP] = self._problem.to_spps()
        n_problems = len(sub_problems)
        for i, sub_problem in enumerate(sub_problems):
            # Add stats for the goals that were explored during other searches.
            if sub_problem.goal in data.explored:
                path = data.path_to(state=sub_problem.goal)
                solution = SolutionSPP(is_valid=True, path=path)
                self._add_solution_spp(goal=sub_problem.goal,   
                                       solution=solution)
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

    def _add_solution_spp(self, goal: State, solution: SolutionSPP) -> None:
        """
        ========================================================================
         Add the Solution of the Sub-Problem to the Data.
        ========================================================================
        """
        self._sub_solutions[goal] = solution
        self._stats.add_stats_goal(goal=goal, stats=solution.stats)
