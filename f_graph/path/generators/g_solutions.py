from f_graph.path.core.solutions import SolutionsPath
from f_graph.path.generators.g_node import GenNode
from f_graph.path.algos.one_to_one.generators.g_solution import GenSolutionOneToOne


class GenSolutionsPath:
    """
    ========================================================================
     Generator for Solutions of Path-Problems.
    ========================================================================
    """

    @staticmethod
    def gen_30_60_90() -> SolutionsPath:
        """
        ========================================================================
         Generate a solution for a 30x60x90 problem.
        ========================================================================
        """
        nodes = GenNode.gen_3x3()
        sols = {node: GenSolutionOneToOne.gen_3x3() for node in nodes}
        return SolutionsPath(is_valid=True, sols=sols, order=list(nodes))
