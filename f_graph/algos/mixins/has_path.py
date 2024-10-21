from f_graph.paths.i_0_base import PathBase, NodePath
from f_graph.paths.i_1_one_to_one import PathOneToOne
from f_graph.paths.i_1_one_to_many import PathOneToMany
from typing import TypeVar, Generic
from enum import Enum

Node = TypeVar('Node', bound=NodePath)


class TypePath(Enum):
    """
    ============================================================================
     Enum-Class for Path options.
    ============================================================================
    """
    ONE_TO_ONE = PathOneToOne
    ONE_TO_MANY = PathOneToMany


class HasPath(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Path-Algorithms with Path objects.
    ============================================================================
    """

    def __init__(self, type_path: TypePath) -> None:
        self._path = type_path.value()

    @property
    def path(self) -> PathBase:
        """
        ========================================================================
         Return the Path object of the Algorithm.
        ========================================================================
        """
        return self._path
