from f_graph.path.algos.one_to_many.problem import ProblemOneToMany, Node
from f_graph.path.algos.one_to_one.algo import AlgoOneToOne, AlgoPath
from f_graph.path.algos.one_to_one.problem import ProblemOneToOne
from f_graph.path.algos.one_to_one.solution import SolutionOneToOne
from f_graph.path.algos.many_to_one.algo import AlgoManyToOne
from f_graph.path.algos.many_to_one.problem import ProblemManyToOne
from f_hs.ds.cache import Cache
from f_graph.path.core.solutions import SolutionsPath


class AlgoForeAndBack(AlgoPath[ProblemOneToMany, SolutionsPath]):
    """
    ============================================================================
     Forward and then Backward Path-Finding Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemOneToMany,
                 depth_boundary: int = 0,
                 verbose: bool = False,
                 name: str = 'Algo Fore-And-Back') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # Init the AlgoPathsuper class.
        AlgoPath.__init__(self,
                          problem=problem,
                          verbose=verbose,
                          name=name)
        self._depth_boundary = depth_boundary

    def run(self) -> SolutionsPath:
        """
        ========================================================================
         Run the Algorithm.
        ========================================================================
        """
        # Init the Solutions dict (key is the goal)
        sols: dict[Node, SolutionOneToOne] = dict()
        # Extract the graph, start and goal from the problem
        graph = self._problem.graph
        start = self._problem.start
        goals = self._problem.goals
        # Get the farthest goal from the start
        goal_farthest = start.farthest(goals)
        print(f'Goal Farthest: {goal_farthest}')
        # Init the forward problem
        problem_forward = ProblemOneToOne(graph=graph,
                                          start=start,
                                          goal=goal_farthest)
        # Run the forward algorithm
        algo_forward = AlgoOneToOne(problem=problem_forward)
        # Get the forward solution
        sol_forward = algo_forward.run()
        sols[goal_farthest] = sol_forward
        if not sol_forward:
            return SolutionsPath(is_valid=False, sols=sols)
        # Create a Cache from the forward explored
        explored = sol_forward.state.explored
        print(f'Forward Explored: {explored}')
        cache = Cache.from_explored(explored=explored)
        # Get the backward goals (except the farthest goal)
        goals_backward = goals - {goal_farthest}
        # Check if some of the goals_backward are already explored
        for goal in goals_backward:
            # If the goal is already explored
            if goal in cache:
                # Create a solution
                sol = SolutionOneToOne(goal=goal)
                # Add the solution to the solutions dict
                sols[goal] = sol
        # Remove the goals that have been reached
        goals_backward -= sols.keys()
        # If there are still goals_backward to explore
        if goals_backward:
            # Init the backward problem
            problem_backward = ProblemManyToOne(graph=graph,
                                                starts=goals_backward,
                                                goal=start)
            # Run the backward algorithm
            algo_backward = AlgoManyToOne(problem=problem_backward,
                                          cache=cache,
                                          depth_boundary=self._depth_boundary)
            # Get the backward solution (with cache)
            sols_backward = algo_backward.run()
            # Update the solutions dict
            sols.update(sols_backward)
            if not sols_backward:
                return SolutionsPath(is_valid=False, sols=sols)
        return SolutionsPath(is_valid=True, sols=sols)
