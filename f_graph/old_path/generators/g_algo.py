from f_graph.old_path.generators.g_problem import GenProblemPath
from f_graph.old_path.generators.g_solution import GenSolutionPath, SolutionPath
from f_graph.old_path.algos.algo import AlgoPath


class GenAlgoPath:
    """
    ============================================================================
     Generator for Algorithms in Path-Finding Problems.
    ============================================================================
    """

    @staticmethod
    def gen_3x3() -> AlgoPath:
        """
        ========================================================================
         Generate an A* algorithm.
        ========================================================================
        """
        class AlgoDemo(AlgoPath):
            def run(self) -> SolutionPath:
                return GenSolutionPath.gen_3x3()

        problem = GenProblemPath.gen_3x3()
        return AlgoDemo(problem=problem)
