from f_graph.path.generators.g_graph import GenGraphPath, NodePath as Node


class GenNode:
    """
    ============================================================================
     Generator for Nodes in Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> tuple[Node, Node, Node]:
        """
        ========================================================================
         Generate a tuple of nodes for a 3x3 problem.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        start = graph[0, 0]
        start.h = 4
        pre_goal = graph[1, 2]
        pre_goal.h = 1
        goal = graph[2, 2]
        goal.h = 0
        goal.parent = pre_goal
        return start, pre_goal, goal

    @staticmethod
    def gen_diagonal(size: int = 3) -> tuple[Node, ...]:
        """
        ========================================================================
         Generate a tuple of nodes for a diagonal problem.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        return tuple(graph[i, j] for i in range(size) for j in range(size) if i == j)
    
    @staticmethod
    def gen_first_row_3x3() -> tuple[Node, ...]:
        """
        ========================================================================
         Generate a tuple of nodes for a 3x3 problem.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        return tuple(graph[0, j] for j in range(3))

