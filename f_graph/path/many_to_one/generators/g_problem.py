from f_graph.path.many_to_one.problem import ProblemManyToOne
from f_graph.path.generators.g_graph import GenGraphPath


class GenProblemManyToOne:
    """
    ============================================================================
     Generator for Many-to-One Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> ProblemManyToOne:

        """
        ========================================================================
         Generate a 3x3 Many-to-One problem.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        starts = [graph[0, 2], graph[2, 2]]
        goal = graph[0, 0]
        return ProblemManyToOne(graph=graph, starts=starts, goal=goal)
