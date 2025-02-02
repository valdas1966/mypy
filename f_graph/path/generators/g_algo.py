from f_graph.path.generators.g_problem import GenProblemPath
from f_graph.path.generators.g_solution import GenSolutionPath, SolutionPath
from f_graph.path.algo import AlgoPath


class GenAlgoPath:
    """
    ============================================================================
     Generator for Algorithms in Path-Finding Problems.
    ============================================================================
    """

    class AlgoDemo(AlgoPath):
        def run(self) -> SolutionPath:
            return GenSolutionPath.gen_3x3()

    @staticmethod
    def gen_3x3() -> AlgoPath:
        """
        ========================================================================
         Generate an A* algorithm.
        ========================================================================
        """
        problem = GenProblemPath.gen_3x3()
        return AlgoDemo(problem=problem)
