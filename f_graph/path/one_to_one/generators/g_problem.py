from f_graph.path.one_to_one.problem import ProblemOneToOne as Problem, Graph, Node
from typing import Type


class GenProblemOneToOne:
    """
    ============================================================================
     Generator for One-to-One Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3(type_node: Type[Node] = Node) -> Problem:
        """
        ========================================================================
         Return a generated ProblemSingle with Graph of 3x3 dimension.
        ========================================================================
        """
        graph = Graph.gen_3x3(type_node=type_node)
        start = graph[0, 0]
        goal = graph[2, 2]
        problem = Problem(graph=graph, start=start, goal=goal)
        problem.pre_goal = graph[1, 2]
        return problem

    @staticmethod
    def gen_4x4(type_node: Type[Node] = Node) -> Problem:
        """
        ========================================================================
         Return a generated ProblemSingle with Graph of 4x4 dimension.
        ========================================================================
        """
        graph = Graph.gen_4x4(type_node=type_node)
        start = graph[0, 0]
        goal = graph[0, 3]
        return Problem(graph=graph, start=start, goal=goal)
