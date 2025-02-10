from f_graph.path.one_to_one.solution import SolutionOneToOne as Solution
from f_graph.path.one_to_one.algo import AlgoOneToOne, TypeAlgo
from f_graph.path.many_to_one.problem import ProblemManyToOne, Node
from f_graph.path.solutions import SolutionsPath as Solutions
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
                 is_shared: bool = True,
                 name: str = 'Path-Algo Many-To-One') -> None:

        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        AlgoPath.__init__(self,
                          problem=problem,
                          cache=cache,
                          type_algo=type_algo,
                          is_shared=is_shared,
                          name=name)

    def run(self) -> Solutions:
        """
        ========================================================================
         Run the algorithm.
        ========================================================================
        """
        sols: dict[Node, Solution] = dict()
        for problem in self._problem.to_singles():
            algo = AlgoOneToOne(problem=problem,
                                cache=self._cache,
                                type_algo=self._type_algo,
                                is_shared=self._is_shared)
            sols[problem.start] = algo.run()
            if not sols[problem.start]:
                return Solutions(is_valid=False, sols=sols)
            path_sol = sols[problem.start].path
            cache_sol = Cache.from_path(path=path_sol)
            self._cache.update(cache_sol)
        return Solutions(sols=sols)

