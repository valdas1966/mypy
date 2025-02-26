from f_graph.path.one_to_one.solution import SolutionOneToOne as Solution
from f_graph.path.one_to_one.algo import AlgoOneToOne, TypeAlgo
from f_graph.path.many_to_one.problem import ProblemManyToOne, Node
from f_graph.path.solutions import SolutionsPath as Solutions
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
                 with_boundary: bool = False,
                 name: str = 'Path-Algo Many-To-One') -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        AlgoPath.__init__(self,
                          problem=problem,
                          name=name)
        self._cache = cache if cache else Cache()
        self._type_algo = type_algo
        self._is_shared = is_shared
        self._boundary = boundary if boundary else Boundary()
        self._is_eager = is_eager
        self._with_boundary = with_boundary

    def run(self) -> Solutions:
        """
        ========================================================================
         Run the algorithm.
        ========================================================================
        """
        sols: dict[Node, Solution] = dict()
        order: list[Node] = list()
        # Divide the MTO-Problem into OTO-Problems.
        for problem in self._problem.to_singles():
            # Store the order of the start nodes.
            order.append(problem.start)
            # For each OTO-Problem, run the OTO-Algorithm.
            algo = AlgoOneToOne(problem=problem,
                                cache=self._cache,
                                type_algo=self._type_algo,
                                boundary=self._boundary,
                                is_shared=False)
            solution = algo.run()
            sols[problem.start] = solution
            # If path is not found, return invalid MTO Solution
            if not solution:
                return Solutions(is_valid=False, sols=sols, order=order)
            # If path is found and is shared:
            #  update the cache with nodes on the optimal path.
            if self._is_shared:
                cache_sol = Cache.from_path(path=solution.path)
                self._cache.update(cache_sol)
                if self._with_boundary:
                    boundary_sol = Boundary.from_path(path=solution.path,
                                                      graph=problem.graph,
                                                      cache=self._cache)
                    self._boundary.update(boundary_sol)
        # Return valid MTO Solution.
        return Solutions(is_valid=True, sols=sols, order=order)

