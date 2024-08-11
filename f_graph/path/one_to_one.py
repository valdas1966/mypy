from f_abstract.mixins.validatable import Validatable
from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class PathOneToOne(Generic[Node], Validatable):
    """
    ============================================================================
     Path-Class for One-to-One Problem.
    ============================================================================
    """

    def __init__(self, goal: Node) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        Validatable.__init__(self, is_valid=False)
        self._goal = goal

    def get(self) -> list[Node]:
        """
        ========================================================================
         Return the Path (List of Nodes).
        ========================================================================
        """
        return self._goal.path_from_root()
