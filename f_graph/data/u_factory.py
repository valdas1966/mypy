from f_graph.data.i_1_core import DataCore, Node
from f_graph.data.i_1_cache import DataCache, DataABC
from f_ds.queues.i_0_base import QueueBase
from typing import Type, TypeVar
from enum import Enum, auto

Data = TypeVar('Data', bound=DataABC)


class TypeData(Enum):
    """
    ============================================================================
     Enum of Data Types.
    ============================================================================
    """
    CORE = auto()
    CACHE = auto()


class FactoryData:
    """
    ============================================================================
     Factory for creating a Data object for Path-Algorithms.
    ============================================================================
    """

    @staticmethod
    def create(type_data: TypeData,
               type_queue: Type[QueueBase],
               cache: set[Node] = None) -> Data:
        """
        ========================================================================
         Create a Data object for Path-Algorithm based on TypeData.
        ========================================================================
        """
        if type_data == TypeData.CORE:
            return DataCore(type_queue=type_queue)
        if type_data == TypeData.CACHE:
            return DataCache(type_queue=type_queue, cache=cache)
