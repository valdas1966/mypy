from f_hs.algo.i_2_dijkstra.main import Dijkstra
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


class Factory:
    """
    ========================================================================
     Factory for Dijkstra test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc() -> Dijkstra:
        """
        ====================================================================
         Dijkstra on linear Graph: A -> B -> C.
        ====================================================================
        """
        return Dijkstra(
            problem=ProblemSPP.Factory.graph_abc()
        )

    @staticmethod
    def graph_no_path() -> Dijkstra:
        """
        ====================================================================
         Dijkstra on Graph with no path to goal.
        ====================================================================
        """
        return Dijkstra(
            problem=ProblemSPP.Factory.graph_no_path()
        )

    @staticmethod
    def graph_start_is_goal() -> Dijkstra:
        """
        ====================================================================
         Dijkstra where start equals goal.
        ====================================================================
        """
        return Dijkstra(
            problem=ProblemSPP.Factory.graph_start_is_goal()
        )

    @staticmethod
    def graph_diamond() -> Dijkstra:
        """
        ====================================================================
         Dijkstra on diamond Graph.
        ====================================================================
        """
        return Dijkstra(
            problem=ProblemSPP.Factory.graph_diamond()
        )

    @staticmethod
    def grid_3x3() -> Dijkstra:
        """
        ====================================================================
         Dijkstra on open 3x3 Grid: (0,0) -> (2,2).
        ====================================================================
        """
        return Dijkstra(
            problem=ProblemGrid.Factory.grid_3x3()
        )

    @staticmethod
    def grid_3x3_obstacle() -> Dijkstra:
        """
        ====================================================================
         Dijkstra on 3x3 Grid with obstacle at (1,1).
        ====================================================================
        """
        return Dijkstra(
            problem=ProblemGrid.Factory.grid_3x3_obstacle()
        )

    @staticmethod
    def grid_3x3_no_path() -> Dijkstra:
        """
        ====================================================================
         Dijkstra on 3x3 Grid with wall blocking all paths.
        ====================================================================
        """
        return Dijkstra(
            problem=ProblemGrid.Factory.grid_3x3_no_path()
        )

    @staticmethod
    def grid_3x3_start_is_goal() -> Dijkstra:
        """
        ====================================================================
         Dijkstra on 3x3 Grid where start equals goal.
        ====================================================================
        """
        return Dijkstra(
            problem=ProblemGrid.Factory.grid_3x3_start_is_goal()
        )
