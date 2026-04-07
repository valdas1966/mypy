from f_hs.algo.i_1_bfs.main import BFS
from f_hs.problem import ProblemSPP
from f_hs.problem.i_1_grid import ProblemGrid


class Factory:
    """
    ========================================================================
     Factory for BFS test instances.
    ========================================================================
    """

    @staticmethod
    def graph_abc() -> BFS:
        """
        ====================================================================
         BFS on linear Graph: A -> B -> C.
        ====================================================================
        """
        return BFS(problem=ProblemSPP.Factory.graph_abc())

    @staticmethod
    def graph_no_path() -> BFS:
        """
        ====================================================================
         BFS on Graph with no path to goal.
        ====================================================================
        """
        return BFS(problem=ProblemSPP.Factory.graph_no_path())

    @staticmethod
    def graph_start_is_goal() -> BFS:
        """
        ====================================================================
         BFS where start equals goal.
        ====================================================================
        """
        return BFS(
            problem=ProblemSPP.Factory.graph_start_is_goal()
        )

    @staticmethod
    def graph_diamond() -> BFS:
        """
        ====================================================================
         BFS on diamond Graph: A -> B -> D, A -> C -> D.
        ====================================================================
        """
        return BFS(problem=ProblemSPP.Factory.graph_diamond())

    @staticmethod
    def grid_3x3() -> BFS:
        """
        ====================================================================
         BFS on open 3x3 Grid: (0,0) -> (2,2).
        ====================================================================
        """
        return BFS(problem=ProblemGrid.Factory.grid_3x3())

    @staticmethod
    def grid_3x3_obstacle() -> BFS:
        """
        ====================================================================
         BFS on 3x3 Grid with obstacle at (1,1).
        ====================================================================
        """
        return BFS(
            problem=ProblemGrid.Factory.grid_3x3_obstacle()
        )

    @staticmethod
    def grid_3x3_no_path() -> BFS:
        """
        ====================================================================
         BFS on 3x3 Grid with wall blocking all paths.
        ====================================================================
        """
        return BFS(
            problem=ProblemGrid.Factory.grid_3x3_no_path()
        )

    @staticmethod
    def grid_3x3_start_is_goal() -> BFS:
        """
        ====================================================================
         BFS on 3x3 Grid where start equals goal.
        ====================================================================
        """
        return BFS(
            problem=ProblemGrid.Factory.grid_3x3_start_is_goal()
        )
