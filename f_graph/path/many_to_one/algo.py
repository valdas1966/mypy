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

    def run(self) -> Solutions:
        """
        ========================================================================
         Run the algorithm.
        ========================================================================
        """
        sols: dict[Node, Solution] = dict()
        # Divide the MTO-Problem into OTO-Problems.
        for problem in self._problem.to_singles():
            # For each OTO-Problem, run the OTO-Algorithm.
            algo = AlgoOneToOne(problem=problem,
                                cache=self._cache,
                                type_algo=self._type_algo,
                                is_shared=self._is_shared)
            sols[problem.start] = algo.run()
            # If path is not found, return invalid MTO Solution
            if not sols[problem.start]:
                return Solutions(is_valid=False, sols=sols)
            # If path is found and is shared:
            #  update the cache with nodes on the optimal path.
            if self._is_shared:
                path_sol = sols[problem.start].path
                cache_sol = Cache.from_path(path=path_sol)
                self._cache.update(cache_sol)
        # Return valid MTO Solution.
        return Solutions(is_valid=True, sols=sols)
