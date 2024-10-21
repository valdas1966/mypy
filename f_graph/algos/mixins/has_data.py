from enum import Enum
from f_graph.data.i_0_path import DataPath, NodePath, TypeQueue
from f_graph.data.i_1_one_to_one import DataOneToOne
from f_graph.data.i_2_one_to_many import DataOneToMany
from typing import Generic, TypeVar

Node = TypeVar('Node', bound=NodePath)


class TypeData(Enum):
    """
    ============================================================================
     Enum-Class with Data-Type options.
    ============================================================================
    """
    ONE_TO_ONE = DataOneToOne
    ONE_TO_MANY = DataOneToMany


class HasData(Generic[Node]):
    """
    ============================================================================
     Mixin-Class for Path-Algorithms with Data.
    ============================================================================
    """

    def __init__(self,
                 type_data: TypeData,
                 type_queue: TypeQueue) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._data = type_data.value(type_queue=type_queue)

    @property
    def data(self) -> DataPath:
        """
        ========================================================================
         Return the Data object of the Algorithm.
        ========================================================================
        """
        return self._data
