from f_graph.path.one_to_many.algo import AlgoOneToMany, TypeAlgo
from f_graph.path.one_to_many.generators.g_problem import GenProblemOneToMany


class GenAlgoOneToMany:
    """
    ===========================================================================
     Generator for One-To-Many Path-Finding Algorithms.
    ===========================================================================
    """

    @staticmethod
    def gen_bfs_shared() -> AlgoOneToMany:
        """
        ========================================================================
         Generate a BFS Algorithm with Shared-Data.
        ========================================================================
        """
        problem = GenProblemOneToMany.gen_3x3()
        return AlgoOneToMany(problem=problem,
                             type_algo=TypeAlgo.BFS,
                             is_shared=True)

    @staticmethod
    def gen_bfs_not_shared() -> AlgoOneToMany:
        """
        ========================================================================
         Generate a BFS Algorithm with Not-Shared-Data.
        ========================================================================
        """
        problem = GenProblemOneToMany.gen_3x3()
        return AlgoOneToMany(problem=problem,
                             type_algo=TypeAlgo.BFS,
                             is_shared=False)

    @staticmethod
    def gen_astar_shared() -> AlgoOneToMany:
        """
        ========================================================================
         Generate an A* Algorithm with Shared-Data.
        ========================================================================
        """
        problem = GenProblemOneToMany.gen_3x3()
        return AlgoOneToMany(problem=problem,
                             type_algo=TypeAlgo.A_STAR,
                             is_shared=True)
    
    @staticmethod
    def gen_astar_not_shared() -> AlgoOneToMany:
        """
        ========================================================================
         Generate an A* Algorithm with Not-Shared-Data.
        ========================================================================
        """
        problem = GenProblemOneToMany.gen_3x3()
        return AlgoOneToMany(problem=problem,
                             type_algo=TypeAlgo.A_STAR,
                             is_shared=False)


astar = GenAlgoOneToMany.gen_astar_shared()
astar.run()