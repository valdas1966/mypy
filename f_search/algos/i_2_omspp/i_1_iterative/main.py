from f_search.algos.i_1_spp.i_0_base.main import (AlgoSPP, ProblemSPP,
                                                  SolutionSPP, DataSPP,
                                                  StatsSPP)
from f_search.algos.i_2_omspp.i_0_base.main import (AlgoOMSPP, ProblemOMSPP,
                                                    SolutionOMSPP)


class IterativeOMSPP(AlgoOMSPP):
    """
    ============================================================================
     Iterative Algorithm for One-to-Many Shortest-Path-Problem.
    ============================================================================
    """
    
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
            # Add stats for the goals that are already explored.
            if sub_problem.goal in data.explored:
                stats = StatsSPP()
                solution = SolutionSPP(is_valid=True,
                                       data=data,
                                       stats=stats)
                self._sub_solutions[sub_problem.goal] = solution
                self._stats.add_goal(goal=sub_problem.goal,
                                     stats=stats)
                continue
            # Run the sub-search.
            name_algo = f'{self._type_algo.__name__} {i+1}/{n_problems}'
            algo = self._type_algo(problem=sub_problem,
                                   data=data,
                                   name=name_algo,
                                   verbose=self._verbose)
            solution = algo.run()
            self._sub_solutions[sub_problem.goal] = solution
            # Add stats for the completed goal.
            self._stats.add_goal(goal=sub_problem.goal,
                                 stats=solution.stats)
            if not solution:
                # If any sub-problem is invalid, the overall solution is invalid
                return self._create_solution(is_valid=False)
            algo._data.generated.push(state=algo._data.best,
                                      cost=algo._data.cost[algo._data.best])
            data = algo._data
        # Return valid solution.
        return self._create_solution(is_valid=True)
