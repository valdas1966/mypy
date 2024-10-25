from abc import ABC
from typing import Generic, TypeVar
from f_abstract.mixins.validatable_public import ValidatablePublic
from f_graph.nodes.i_1_path import NodePath

Node = TypeVar('Node', bound=NodePath)


class PathBase(ABC, Generic[Node], ValidatablePublic):
    """
    ============================================================================
     Base-Class of Path for Path-Algorithms.
    ============================================================================
    """

    def __init__(self):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        ValidatablePublic.__init__(self, is_valid=False)

    def get(self, goal: Node) -> list[Node]:
        """
        ========================================================================
         Return an Optimal Path founded from Start to the received Goal.
        ========================================================================
        """
        return goal.path_from_root()
