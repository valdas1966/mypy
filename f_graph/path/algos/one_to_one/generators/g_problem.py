from f_graph.path.algos.one_to_one.problem import ProblemOneToOne as Problem
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
    def gen_4x4() -> Problem:
        """
        ========================================================================
         Return a generated ProblemSingle with Graph of 4x4 dimension.
        ========================================================================
        """
        graph = GenGraphPath.gen_4x4()
        start = graph[0, 0]
        goal = graph[3, 3]
        problem = Problem(graph=graph, start=start, goal=goal)
        return problem

    @staticmethod
    def boundary_4x4() -> Problem:
        """
        ========================================================================
         Return a generated ProblemSingle with Graph of 4x4 dimension.
        ========================================================================
        """
        graph = GenGraphPath.gen_4x4()
        start = graph[2, 2]
        goal = graph[2, 0]
        return Problem(graph=graph, start=start, goal=goal)
        
