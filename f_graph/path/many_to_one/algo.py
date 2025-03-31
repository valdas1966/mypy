from f_graph.path.one_to_one.solution import SolutionOneToOne as Solution
from f_graph.path.one_to_one.algo import AlgoOneToOne, TypeAlgo
from f_graph.path.heuristic import Heuristic, TypeHeuristic
from f_graph.path.many_to_one.problem import ProblemManyToOne, Node
from f_graph.path.many_to_one.solutions import SolutionsManyToOne as Solutions
from f_graph.path.boundary import Boundary
from f_graph.path.algo import AlgoPath
from f_graph.path.cache import Cache


class AlgoManyToOne(AlgoPath[ProblemManyToOne, Solutions]):
    """
    ============================================================================
     Many-To-One Path-Finding Algorithm.
    ============================================================================
    """

    def __init__(self,
                 problem: ProblemManyToOne,
                 cache: Cache = None,
                 type_algo: TypeAlgo = TypeAlgo.A_STAR,
                 boundary: Boundary = None,
                 is_eager: bool = False,
                 is_shared: bool = True,
                 depth_boundary: int = 0,
                 verbose: bool = True,
                 name: str = 'Path-Algo Many-To-One') -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        AlgoPath.__init__(self,
                          problem=problem,
                          verbose=verbose,
                          name=name)
        self._cache = cache if cache else Cache()
        self._type_algo = type_algo
        self._is_shared = is_shared
        self._boundary = boundary if boundary else Boundary()
        self._is_eager = is_eager
        self._depth_boundary = depth_boundary

    def run(self) -> Solutions:
        """
        ========================================================================
         Run the algorithm.
        ========================================================================
        """
        sols: dict[Node, Solution] = dict()
        exploited: set[Node] = set()
        # Divide the MTO-Problem into OTO-Problems.
        problems = self._problem.to_singles()
        for i, problem in enumerate(problems):
            # For each OTO-Problem, run the OTO-Algorithm.
            algo = AlgoOneToOne(problem=problem,
                                cache=self._cache,
                                type_algo=self._type_algo,
                                boundary=self._boundary,
                                is_shared=False,
                                verbose=False)
            solution = algo.run()
            sols[problem.start] = solution
            # If path is not found, return invalid MTO Solution
            if not solution:
                return Solutions(is_valid=False, sols=sols)
            # If path is found and is shared:
            #  update the cache with nodes on the optimal path.
            if self._is_shared and i < len(problems) - 1:
                cache_sol = Cache.from_path(path=solution.path)
                self._cache.update(cache_sol)
                if self._depth_boundary:
                    heuristic = Heuristic(graph=problem.graph,
                                          goal=problem.goal,
                                          type_heuristic=TypeHeuristic.MANHATTAN)
                    boundary_sol = Boundary.from_path(path=solution.path,
                                                      graph=problem.graph,
                                                      heuristic=heuristic,
                                                      cache=self._cache,
                                                      exploited=exploited,
                                                      depth=self._depth_boundary)
                    exploited.update(set(solution.path))
                    self._boundary.update(boundary_sol)
                    for key, value in boundary_sol.stats_changed.items():
                        self._boundary.stats_changed[key] += value

        # Return valid MTO Solution.
        return Solutions(is_valid=True,
                         sols=sols,
                         changed=self._boundary.stats_changed)
