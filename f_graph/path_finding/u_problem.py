from f_graph.path_finding.problem import Problem
from f_graph.graphs.u_1_grid import UGraphGrid, NodePathCell as Node
from typing import Type


class GenProblemPath:
    """
    ============================================================================
     Path-Problem Generator.
    ============================================================================
    """

    @staticmethod
    def random(rows: int = 100,
               pct_valid: int = 75,
               goals: int = 1,
               type_node: Type[Node] = Node) -> Problem:
        """
        ========================================================================
         Generate a random Path-Problem.
        ========================================================================
        """
        graph = UGraphGrid.generate(rows=rows,
                                    pct_valid=pct_valid,
                                    type_node=type_node)
        start, *goals = graph.sample(size=goals+1)
        return Problem(graph=graph, start=start, goals=goals)

    @staticmethod
    def one_goal_3x3(type_node: Type[Node] = Node) -> Problem:
        """
        ========================================================================
         Generate a classic One-to-One problem on small grid (3x3) without
          obstacles, when the Start is at [0,0] and the Goal is at [2,2].
        ========================================================================
        """
        graph = UGraphGrid.generate(rows=3,
                                    pct_valid=100,
                                    type_node=type_node)
        start = graph[0, 0]
        goals = {graph[2, 2]}
        return Problem(graph=graph, start=start, goals=goals)

    @staticmethod
    def multi_goals_3x3(type_node: Type[Node] = Node) -> Problem:
        """
        ========================================================================
         Generate a classic One-to-Many problem on small grid (3x3) without
          obstacles, when Start is at [0,0] and Goals are at the far corners.
        ========================================================================
        """
        graph = UGraphGrid.generate(rows=3,
                                    pct_valid=100,
                                    type_node=type_node)
        start = graph[0, 0]
        goals = {graph[0, 2], graph[2, 2]}
        return Problem(graph=graph, start=start, goals=goals)