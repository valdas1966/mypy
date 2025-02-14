from f_graph.path.one_to_one.problem import ProblemOneToOne as Problem
from f_graph.path.generators.g_graph import GenGraphPath


class GenProblemOneToOne:
    """
    ============================================================================
     Generator for One-to-One Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> Problem:
        """
        ========================================================================
         Return a generated ProblemSingle with Graph of 3x3 dimension.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        start = graph[0, 0]
        goal = graph[2, 2]
        problem = Problem(graph=graph, start=start, goal=goal)
        return problem
    
    @staticmethod
    
