from f_graph.paths.i_0_base import PathBase, NodePath
from f_graph.problems.i_2_one_to_one import ProblemOneToOne
from typing import TypeVar

Problem = TypeVar('Problem', bound=ProblemOneToOne)
Node = TypeVar('Node', bound=NodePath)


class PathOneToOne(PathBase[Problem, Node]):
    """
    ============================================================================
     Path of One-to-One Problem.
    ============================================================================
    """

    def get(self) -> list[Node]:
        """
        ========================================================================
         Return a Path from Start to Goal.
        ========================================================================
        """
        return self.problem.goal.path_from_root()
