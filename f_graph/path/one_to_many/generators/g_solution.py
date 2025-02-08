from f_graph.path.one_to_one.generators.g_solution import GenSolutionOneToOne
from f_graph.path.one_to_many.solution import SolutionOneToMany
from f_graph.path.generators.g_node import GenNode


class GenSolutionOneToMany:
    """
    ========================================================================
     Generator for One-To-Many Path-Problem.
    ========================================================================
    """

    @staticmethod
    def gen_3x3() -> SolutionOneToMany:
        """
        ========================================================================
         Generate a 3x3 solution.
        ========================================================================
        """
        nodes = GenNode.gen_3x3()
        sols = {node: GenSolutionOneToOne.gen_3x3() for node in nodes}
        return SolutionOneToMany(is_valid=True, sols=sols)


sol = GenSolutionOneToMany.gen_3x3()
for node, stats in sol.stats.items():
    print(node)
    print(stats)
print(sol.explored)
