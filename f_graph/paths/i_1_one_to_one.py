from f_graph.paths.i_0_base import PathBase, NodePath
from typing import TypeVar

Node = TypeVar('Node', bound=NodePath)


class PathOneToOne(PathBase[Node]):
    """
    ============================================================================
     Path of One-to-One Problem.
    ============================================================================
    """

    def __init__(self, goal: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        PathBase.__init__(self)
        self._goal = goal

    def get(self) -> list[Node]:
        """
        ========================================================================
         Return a Path from Start to Goal.
        ========================================================================
        """
        return self._goal.path_from_root()
