from f_graph.path.generators.g_stats import GenStatsPath
from f_graph.path.solution import SolutionPath


class GenSolutionPath:
    """
    ============================================================================
     Generator for Solutions in Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> SolutionPath:
        """
        ========================================================================
         Generate a solution for a 3x3 problem.
        ========================================================================
        """
        stats = GenStatsPath.gen_10x20()
        return SolutionPath(is_valid=True, stats=stats)
    
