from f_graph.path.one_to_many.problem import ProblemOneToMany
from f_graph.path.generators.g_graph import GenGraphPath, Graph
from f_ds.grids.grid import Grid, Cell


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
        graph = GenGraphPath.gen_3x3()
        start = graph[0, 0]
        goals = [graph[0, 2], graph[2, 0]]
        return ProblemOneToMany(graph=graph, start=start, goals=goals)
    
    @staticmethod
    def corner_3_goals() -> ProblemOneToMany:
        """
        ========================================================================
         Generate a 3x3 Grid Path-Finding Problem with 3 goals.
        ========================================================================
        """
        grid = Grid(4)
        Cell.invalidate([grid[0][1], grid[1][1], grid[2][1]])
        graph = Graph(grid=grid)
        start = graph[0, 0]
        goals = [graph[0, 3], graph[0, 2], graph[1, 3]]
        return ProblemOneToMany(graph=graph, start=start, goals=goals)

