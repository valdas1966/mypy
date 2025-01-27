from f_graph.path.one_to_many.problem import ProblemOneToMany, Graph, Node


class GenProblemOneToMany:
    """
    ===========================================================================
     Generator for One-To-Many Pathfinding Problems.
    ===========================================================================
    """

    @staticmethod
    def gen_3x3() -> ProblemOneToMany:
        """
        ========================================================================
         Generate a 3x3 Grid Path-Finding Problem.
        ========================================================================
        """
        graph = Graph.gen_3x3()
        start = graph[0, 0]
        goals = [graph[0, 2], graph[2, 0]]
        return ProblemOneToMany(graph=graph, start=start, goals=goals)
