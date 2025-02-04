from f_graph.path.solutions import SolutionsPath
from f_graph.path.generators.g_solution import GenSolutionPath
from f_graph.path.generators.g_node import GenNode


class GenSolutionsPath:
    """
    ========================================================================
     Generator for Solutions of Path-Problems.
    ========================================================================
    """

    def gen_30_60_90() -> SolutionsPath:
        """
        ========================================================================
         Generate a solution for a 30x60x90 problem.
        ========================================================================
        """
        nodes = GenNode.gen_3x3()
        sols = {node: GenSolutionPath.gen_3x3() for node in nodes}
        return SolutionsPath(sols)
