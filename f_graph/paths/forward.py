from f_abstract.mixins.validatable_public import ValidatablePublic
from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class PathForward(Generic[Node], ValidatablePublic):
    """
    ============================================================================
     Class for Forward-Path in Graph-Problem.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ValidatablePublic.__init__(self, is_valid=False)

    def get(self, goal: Node = None) -> list[Node]:
        """
        ========================================================================
         Return the Path (List of Nodes).
        ========================================================================
        """
        if goal:
            return goal.path_from_root()
        else:
            return self._goal.path_from_start()
