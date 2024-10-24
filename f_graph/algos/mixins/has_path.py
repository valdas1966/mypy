from f_graph.paths.i_0_base import PathBase, NodePath
from typing import TypeVar, Generic

Node = TypeVar('Node', bound=NodePath)


class HasPath(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Path-Algorithms with Path objects.
    ============================================================================
    """

    def __init__(self) -> None:
        self._path = PathBase()

    @property
    def path(self) -> PathBase:
        """
        ========================================================================
         Return the Path object of the Algorithm.
        ========================================================================
        """
        return self._path
