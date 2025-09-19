from f_graph.path.algos.one_to_one.algo import AlgoOneToOne, TypeAlgo
from f_graph.path.algos.one_to_one.generators.g_problem import GenProblemOneToOne


class GenAlgoOneToOne:
    """
    ============================================================================
     Generator for Path-Algorithms.
    ============================================================================
    """
    
    @staticmethod
    def gen_3x3_bfs() -> AlgoOneToOne:
        """
        ========================================================================
         Generate a 3x3 BFS-Algorithm.
        ========================================================================
        """
        problem = GenProblemOneToOne.gen_3x3()
        algo = AlgoOneToOne(problem=problem, type_algo=TypeAlgo.BFS)
        return algo
    
    @staticmethod
    def gen_3x3_astar() -> AlgoOneToOne:
        """
        ========================================================================
         Generate a 3x3 A*-Algorithm.
        ========================================================================
        """ 
        problem = GenProblemOneToOne.gen_3x3()
        algo = AlgoOneToOne(problem=problem, type_algo=TypeAlgo.A_STAR)
        return algo

