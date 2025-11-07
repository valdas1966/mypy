from f_graph.old_path.generators.g_graph import GenGraphPath
from f_graph.old_path.core.problem import ProblemPath


class GenProblemPath:
    """
    ============================================================================
     ProblemPath Generator.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> ProblemPath:
        """
        ========================================================================
         Generate a 3x3 ProblemPath.
        ========================================================================
        """
        graph = GenGraphPath.gen_3x3()
        return ProblemPath(graph=graph)
