from f_graph.nodes.i_1_path import NodePath
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class PathOneToOne(Generic[Node]):
    """
    ============================================================================
     Path-Class for One-to-One Problem.
    ============================================================================
    """

    def __init__(self, goal: Node):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._goal = goal
        self._is_found = False

    @property
    def is_found(self) -> bool:
        """
        ========================================================================
         Return True if the Path is found.
        ========================================================================
        """
        return self._is_found

    def set_found(self) -> None:
        """
        ========================================================================
         Set that the Path is found.
        ========================================================================
        """
        self._is_found = False

    def get(self) -> list[Node]:
        """
        ========================================================================
         Return the Path (List of Nodes).
        ========================================================================
        """
        return self._goal.path_from_root()
