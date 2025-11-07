from f_graph.old_path.algos.one_to_many.problem import ProblemOneToMany
from f_graph.old_path.generators.g_graph import GenGraphPath, Graph
from f_ds.old_grids.old_grid import Grid, Cell
import random


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


    @staticmethod
    def gen_random(rows: int,
                   n_goals: int,
                   pct_invalid: int = None) -> ProblemOneToMany:
        """
        ========================================================================
         Generate a random Path-Finding Problem.
        ========================================================================
        """
        if pct_invalid is None:
            pct_invalid = random.randint(0, 70)
        graph = GenGraphPath.gen_random(rows=rows,
                                        pct_invalid=pct_invalid)
        start, *goals = graph.sample(size=n_goals + 1)
        return ProblemOneToMany(graph=graph, start=start, goals=goals)
