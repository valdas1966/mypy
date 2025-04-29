from f_graph.path.algo import Solution
from f_graph.path.one_to_many.algo import ProblemOneToMany, Node
from f_graph.path.one_to_one.algo import AlgoOneToOne, AlgoPath
from f_graph.path.one_to_one.problem import ProblemOneToOne
from f_graph.path.one_to_one.solution import SolutionOneToOne
from f_graph.path.many_to_one.algo import AlgoManyToOne
from f_graph.path.many_to_one.problem import ProblemManyToOne
from f_graph.path.path import Path
from f_graph.path.cache import Cache
from f_graph.path.solutions import SolutionsPath


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
        graph = self.problem.graph
        start = self.problem.start
        goals = self.problem.goals
        # Get the farthest goal from the start
        goal_farthest = start.farthest(goals)
        # Init the forward problem
        problem_forward = ProblemOneToOne(graph=graph,
                                          start=start,
                                          goal=goal_farthest)
        # Run the forward algorithm
        algo_forward = AlgoOneToOne(problem=problem_forward)
        # Get the forward solution
        sols_forward = algo_forward.run()
        explored = sols_forward.explored
        cache = Cache.from_explored(explored=explored)
        # Get the backward goals (except the farthest goal)
        goals_backward = goals - {goal_farthest}
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
        # Get the backward solution
        goal = self.problem.goal
        if goal_farthest == goal:
            sols[goal] = SolutionOneToOne(goal=goal,
                                          path=Path(goal))
        else:
            sols[goal] = SolutionOneToOne(goal=goal,
                                          path=Path(goal))

       