from f_graph.paths.i_0_base import PathBase, NodePath
from f_graph.problems.i_2_one_to_many import ProblemOneToMany
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToMany)
Node = TypeVar('Node', bound=NodePath)


class PathOneToMany(PathBase[Problem, Node]):
    """
    ============================================================================
     Path of One-to-Many Problem.
    ============================================================================
    """

    def get(self, goal: Node) -> list[Node]:
        """
        ========================================================================
         Return a Path from Start to a given Goal.
        ========================================================================
        """
        return goal.path_from_root()
