from f_graph.path.many_to_one.algo import AlgoManyToOne, TypeAlgo
from f_graph.path.many_to_one.generators.g_problem import GenProblemManyToOne


class GenAlgoManyToOne:
    """
    ============================================================================
     Generator for Many-To-One Path-Finding Algorithms.
    ============================================================================
    """

    @staticmethod
    def gen_3x3_bfs(is_shared: bool) -> AlgoManyToOne:
        """
        ========================================================================
         Generate a BFS-Algorithm for a 3x3-Grid-Problem.
        ========================================================================
        """
        problem = GenProblemManyToOne.gen_3x3()
        algo = AlgoManyToOne(problem=problem,
                             type_algo=TypeAlgo.BFS,
                             is_shared=is_shared)
        return algo

    @staticmethod
    def gen_3x3_astar(is_shared: bool) -> AlgoManyToOne:
        """
        ========================================================================
         Generate an A*-Algorithm for a 3x3-Grid-Problem.
        ========================================================================
        """
        problem = GenProblemManyToOne.gen_3x3()
        algo = AlgoManyToOne(problem=problem,
                             type_algo=TypeAlgo.A_STAR,
                             is_shared=is_shared)
        return algo

    @staticmethod
    def spec_4x4() -> AlgoManyToOne:
        """
        ========================================================================
         Generate an A*-Algorithm for a 4x4-Grid Many-To-One Problem.
        ========================================================================
        """
        problem = GenProblemManyToOne.spec_4x4()
        algo = AlgoManyToOne(problem=problem,
                             type_algo=TypeAlgo.A_STAR,
                             is_shared=True,
                             is_eager=True,
                             with_boundary=True)
        return algo
