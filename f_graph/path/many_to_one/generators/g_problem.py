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
    
    @staticmethod
    def gen_3x3x3() -> ProblemManyToOne:
        """
        ========================================================================
         Generate a 3x3 Many-to-One problem with 3 starts.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        starts = [graph[0, 2], graph[2, 2], graph[2, 0]]
        goal = graph[0, 0]
        return ProblemManyToOne(graph=graph, starts=starts, goal=goal)

    @staticmethod
    def gen_random(rows: int,
                   pct_invalid: int,
                   num_starts: int) -> ProblemManyToOne:
        """
        ========================================================================
         Generate a random Many-to-One problem.
        ========================================================================
        """
        graph = GenGraphPath.gen_random(rows=rows,
                                        pct_invalid=pct_invalid)
        nodes = graph.sample(num_starts + 1)
        starts = nodes[:num_starts]
        goal = nodes[-1]
        return ProblemManyToOne(graph=graph, starts=starts, goal=goal)
